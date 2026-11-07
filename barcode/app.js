(() => {
  'use strict';
  const form = document.getElementById('generator-form');
  const formatSelect = document.getElementById('format');
  const dataInput = document.getElementById('barcode-data');
  const preview = document.getElementById('preview');
  const status = document.getElementById('status');
  const downloadPng = document.getElementById('download-png');
  const downloadSvg = document.getElementById('download-svg');
  const characterCount = document.getElementById('character-count');
  const dataHint = document.getElementById('data-hint');
  const captionRow = document.getElementById('caption-row');
  const widthGroup = document.getElementById('width-group');
  const heightGroup = document.getElementById('height-group');
  let currentSvg = '';
  let currentFormat = '';
  const qrOptions = { errorCorrectionLevel: 'M', margin: 3, width: 320 };
  const isQr = () => formatSelect.value === 'QR';

  function updateFormatFields() {
    const qr = isQr();
    captionRow.hidden = qr;
    widthGroup.hidden = qr;
    heightGroup.hidden = qr;
    dataInput.maxLength = qr ? 2500 : 120;
    dataHint.textContent = qr ? 'Links, text, and other content supported.' : 'Allowed characters depend on the selected barcode type.';
    characterCount.textContent = `${dataInput.value.length} / ${dataInput.maxLength}`;
  }
  function setStatus(message, isError = false) {
    status.textContent = message;
    status.classList.toggle('status-error', isError);
  }
  function setDownloads(enabled) {
    downloadPng.disabled = !enabled;
    downloadSvg.disabled = !enabled;
  }
  function makeBarcode() {
    const value = dataInput.value.trim();
    if (!value) return Promise.reject(new Error('Please enter text or a number first.'));
    if (isQr()) {
      if (!window.QRCode) return Promise.reject(new Error('The QR code library could not be loaded. Check your internet connection and try again.'));
      return QRCode.toString(value, { ...qrOptions, color: { dark: `${document.getElementById('foreground').value}ff`, light: `${document.getElementById('background').value}ff` } });
    }
    if (!window.JsBarcode) return Promise.reject(new Error('The barcode library could not be loaded. Check your internet connection and try again.'));
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const options = { format: formatSelect.value, lineColor: document.getElementById('foreground').value, background: document.getElementById('background').value,
      width: Number(document.getElementById('bar-width').value), height: Number(document.getElementById('bar-height').value),
      displayValue: document.getElementById('show-caption').checked, margin: 12, textMargin: 6, font: 'Arial', fontSize: 16,
      valid: (valid) => { if (!valid) throw new Error(`“${formatSelect.options[formatSelect.selectedIndex].text}” cannot encode this value. Check the content and try again.`); } };
    try { JsBarcode(svg, value, options); }
    catch (error) {
      if (error instanceof Error && error.message) return Promise.reject(error);
      return Promise.reject(new Error('This value is not valid for the selected barcode type. Check the format requirements and try again.'));
    }
    return Promise.resolve(new XMLSerializer().serializeToString(svg));
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    setDownloads(false);
    currentSvg = '';
    setStatus('Generating your barcode…');
    try {
      const svgMarkup = await makeBarcode();
      const parsed = new DOMParser().parseFromString(svgMarkup, 'image/svg+xml');
      const svg = parsed.documentElement;
      if (parsed.querySelector('parsererror') || svg.localName !== 'svg') throw new Error('The barcode could not be generated. Please check your input and try again.');
      currentSvg = new XMLSerializer().serializeToString(svg);
      currentFormat = formatSelect.value;
      preview.replaceChildren(document.importNode(svg, true));
      setDownloads(true);
      setStatus('Barcode generated successfully.');
    } catch (error) { setStatus(error instanceof Error ? error.message : 'Something went wrong. Please try again.', true); }
  });
  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = filename; document.body.append(link); link.click(); link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  const safeFormatName = () => currentFormat.toLowerCase().replace(/[^a-z0-9-]/g, '-') || 'barcode';
  downloadSvg.addEventListener('click', () => { if (currentSvg) downloadBlob(new Blob([currentSvg], { type: 'image/svg+xml;charset=utf-8' }), `${safeFormatName()}-barcode.svg`); });
  downloadPng.addEventListener('click', () => {
    if (!currentSvg) return;
    const objectUrl = URL.createObjectURL(new Blob([currentSvg], { type: 'image/svg+xml;charset=utf-8' }));
    const image = new Image();
    image.onload = () => {
      const canvas = document.createElement('canvas'); canvas.width = image.naturalWidth || 640; canvas.height = image.naturalHeight || 400;
      const context = canvas.getContext('2d');
      if (!context) { URL.revokeObjectURL(objectUrl); setStatus('Your browser could not prepare the PNG. Please try downloading SVG instead.', true); return; }
      context.drawImage(image, 0, 0, canvas.width, canvas.height); URL.revokeObjectURL(objectUrl);
      canvas.toBlob((blob) => { if (blob) downloadBlob(blob, `${safeFormatName()}-barcode.png`); else setStatus('PNG export failed. Please try downloading SVG instead.', true); }, 'image/png');
    };
    image.onerror = () => { URL.revokeObjectURL(objectUrl); setStatus('PNG export failed. Please try downloading SVG instead.', true); };
    image.src = objectUrl;
  });
  formatSelect.addEventListener('change', updateFormatFields);
  dataInput.addEventListener('input', () => { characterCount.textContent = `${dataInput.value.length} / ${dataInput.maxLength}`; });
  document.getElementById('year').textContent = new Date().getFullYear();
  updateFormatFields();
  form.requestSubmit();
})();
