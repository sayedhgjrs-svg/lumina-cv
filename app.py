import base64
import html
import json
import zlib
from urllib.parse import quote

import streamlit as st

st.set_page_config(page_title="Lumina CV | Free Resume Builder", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# =====================================================================
# بيانات التواصل (غيّرها بقيمك الحقيقية) / Contact details (edit these)
# =====================================================================
CONTACT = {
    "email": "sayedhgjrs@gmail.com",      # e.g. "hello@yourdomain.com"
    "phone": "+20 109 649 4090",      # e.g. "+1 555 000 0000"
    "linkedin": "https://www.linkedin.com/in/sayed-hagrs",   # full URL
    "github": "https://github.com/sayedhgjrs-svg",     # full URL
    "x": "https://x.com/sayedhgjrs2h",          # full URL
    "loc": {"ar": "", "en": ""},
}

# رابط الإعلان (اتركه فاضي "" لو عاوز تشيله). بيظهر في الفوتر فقط وبعلامة واضحة إنه إعلان.
AD_LINK = "https://uplcm.com/4/11097841"

# بانر إعلاني ثابت (صورة + رابط) بياخدهم من برنامج الإحالة/الإعلانات. الفاضي لا يظهر.
# مثال: AD_BANNER = {"img": "https://.../banner-300x250.png", "url": "https://رابطك-الخاص", "alt": "Advertisement", "width": 300}
# ملاحظة أمان: بندعم صورة + رابط فقط. ماتحطش كود سكريبت من شبكة إعلانات هنا، لأنه ممكن يقرا بيانات الزائر.
AD_BANNER = {"img": "", "url": "", "alt": "Advertisement", "width": 300}

# روابط الإحالة (Affiliate): أضف روابطك الحقيقية هنا بعد ما تسجل في برامج الإحالة. القائمة الفاضية = لا يظهر قسم الموارد.
# مثال: {"title": {"ar": "اسم الخدمة", "en": "Service name"}, "desc": {"ar": "وصف قصير", "en": "Short description"}, "url": "https://..."}
AFFILIATES = []

# أدواتك الأخرى (كروت تعريفية بمواقعك). ضع رابط الأداة في "url". الفاضي لا يظهر.
OTHER_TOOLS = [
    {"icon": "🖼️",
     "title": {"ar": "ضغط وتغيير حجم الصور", "en": "Image Resizer & Compressor"},
     "desc": {"ar": "صغّر حجم صورتك مباشرة في المتصفح بمنزلقات للجودة، ثم حمّلها PNG أو JPG.",
              "en": "Shrink your image right in the browser with quality sliders, then download it as PNG or JPG."},
     "url": "https://tools.pulsesave.net/image-resizer/"},
]

PAGES = ["home", "builder", "templates", "how", "contact"]
TPLS = ["glass", "classic", "side"]
FIELDS = ["name", "title", "email", "phone", "city", "links", "summary", "exp", "edu",
          "projects", "courses", "skills", "langs"]

THEMES = [
    {"a": "#00f5d4", "b": "#7b2ff7", "bg": "#070b14"},
    {"a": "#c77dff", "b": "#ff5db1", "bg": "#0d0716"},
    {"a": "#ffd166", "b": "#ef8354", "bg": "#100c06"},
    {"a": "#4cc9f0", "b": "#4361ee", "bg": "#060c1a"},
]

# =====================================================================
# النصوص: ترجمة كاملة لكل لغة
# =====================================================================
T = {
    "ar": {
        "dir": "rtl", "ff": "'Cairo','Segoe UI',sans-serif", "ffs": "'Cairo','Segoe UI',sans-serif",
        "nav": ["الرئيسية", "منشئ السيرة", "القوالب", "كيف يعمل", "تواصل معنا"],
        "lang_label": "اللغة",
        "hero_title": "اصنع سيرتك الذاتية بشكل يلفت الانتباه",
        "hero_sub": "املأ بياناتك، اختر القالب واللون، وحمّل سيرة ذاتية جاهزة للطباعة خلال دقائق. ثنائية اللغة، ومجانية بالكامل.",
        "cta_start": "ابدأ الآن", "cta_tpl": "تصفح القوالب",
        "prev_title": "هكذا ستبدو سيرتك",
        "feat_title": "كل ما تحتاجه في مكان واحد",
        "features": [
            ("🌐", "عربي وإنجليزي بالكامل", "كل نص يتغير مع اللغة، والعربية تعمل من اليمين لليسار تلقائيًا."),
            ("🎨", "ثلاثة قوالب وأربعة ألوان", "زجاجي، كلاسيكي، وعمودين. غيّر المظهر بضغطة واحدة."),
            ("🖼️", "صورة شخصية", "ارفع صورتك لتظهر داخل السيرة وفي الملف المحمّل."),
            ("🖨️", "جاهزة للطباعة وPDF", "ملف بتصميم أبيض نظيف تحفظه PDF من المتصفح."),
            ("🧩", "أقسام كاملة", "نبذة، خبرات، تعليم، مشاريع، دورات، مهارات، لغات وروابط."),
            ("🔒", "بدون حساب", "لا تسجيل ولا قاعدة بيانات. بياناتك تبقى في جلستك فقط."),
        ],
        "steps_title": "ثلاث خطوات فقط",
        "steps": [
            ("املأ بياناتك", "اكتب معلوماتك في المنشئ وشاهد المعاينة تتحدث فورًا."),
            ("اختر التصميم", "قالب ولون يناسبان مجالك."),
            ("حمّل واطبع", "حمّل الملف ثم احفظه PDF من المتصفح."),
        ],
        "b_title": "منشئ السيرة الذاتية", "b_sub": "عدّل البيانات على الجانب وشاهد النتيجة مباشرة.",
        "s_design": "التصميم", "tpl_label": "القالب", "theme_label": "اللون",
        "s_personal": "البيانات الشخصية", "s_content": "المحتوى", "s_extra": "أقسام إضافية",
        "f_name": "الاسم الكامل", "f_title": "المسمى الوظيفي", "f_email": "البريد الإلكتروني",
        "f_phone": "رقم الهاتف", "f_city": "المدينة",
        "f_links": "الروابط (رابط في كل سطر)", "f_summary": "نبذة مهنية",
        "f_exp": "الخبرات العملية (خبرة في كل سطر)", "f_edu": "التعليم والشهادات (عنصر في كل سطر)",
        "f_projects": "المشاريع (مشروع في كل سطر)", "f_courses": "الدورات (دورة في كل سطر)",
        "f_skills": "المهارات (افصل بينها بفاصلة)", "f_langs": "اللغات (افصل بينها بفاصلة)",
        "photo": "ارفع صورتك الشخصية", "photo_ok": "تم رفع الصورة", "photo_rm": "حذف الصورة",
        "h_summary": "النبذة المهنية", "h_exp": "الخبرات العملية", "h_edu": "التعليم والشهادات",
        "h_projects": "المشاريع", "h_courses": "الدورات", "h_skills": "المهارات", "h_langs": "اللغات",
        "download": "تحميل السيرة الذاتية", "tip": "افتح الملف ثم اضغط Ctrl+P واختر Save as PDF.",
        "tpl_names": {"glass": "زجاجي", "classic": "كلاسيكي", "side": "عمودان"},
        "tpl_desc": {"glass": "خلفية داكنة متوهجة للعرض على الشاشة. عند التحميل يتحول إلى أبيض نظيف.",
                     "classic": "عمود واحد بسيط وواضح، الأنسب لأنظمة فرز السير الذاتية.",
                     "side": "شريط جانبي ملون للمعلومات والمهارات ومحتوى رئيسي بجانبه."},
        "theme_names": ["سيان نيون", "بنفسجي ملكي", "ذهبي فاخر", "أزرق محيطي"],
        "t_title": "القوالب", "t_sub": "اختر التصميم الأقرب لمجالك، ويمكنك تغييره لاحقًا.",
        "t_use": "استخدم هذا القالب", "t_cur": "القالب الحالي",
        "how_title": "كيف يعمل", "faq_title": "الأسئلة الشائعة",
        "faqs": [
            ("هل المنصة مجانية؟", "نعم، مجانية بالكامل ولا تحتاج إلى حساب."),
            ("هل بياناتي محفوظة؟", "لا تُكتب بياناتك في أي قاعدة بيانات. تبقى في جلستك أثناء فتح الصفحة، وتختفي عند إغلاقها أو تحديثها، لذلك حمّل ملفك قبل الخروج."),
            ("كيف أحصل على ملف PDF؟", "حمّل الملف، افتحه في المتصفح، اضغط Ctrl+P ثم اختر Save as PDF."),
            ("هل يتم ترجمة ما أكتبه عند تغيير اللغة؟", "لا. لكل لغة حقولها الخاصة، فاكتب النسخة العربية والإنجليزية كل واحدة على حدة."),
            ("ما صيغ الصور المدعومة؟", "PNG وJPG وJPEG وWebP."),
            ("أي قالب أنسب لأنظمة فرز السير؟", "القالب الكلاسيكي لأنه عمود واحد بنص بسيط بدون عناصر معقدة."),
            ("هل أستطيع مشاركة سيرتي برابط؟", "نعم. اضغط إنشاء رابط للمشاركة في المنشئ وانسخ الرابط. بياناتك تُحفظ داخل الرابط نفسه، وأي شخص معه الرابط يستطيع رؤيتها."),
        ],
        "priv_title": "الخصوصية", "priv_text": "لا نجمع بياناتك الشخصية ولا نبيعها ولا نخزنها في قاعدة بيانات. تُعالج المعلومات التي تكتبها داخل جلستك فقط لإنشاء سيرتك.",
        "terms_title": "شروط الاستخدام", "terms_text": "الخدمة مقدمة كما هي. أنت المسؤول عن صحة المعلومات التي تضعها في سيرتك الذاتية.",
        "c_title": "تواصل معنا", "c_sub": "عندك اقتراح أو واجهت مشكلة؟ راسلنا.",
        "c_email": "البريد الإلكتروني", "c_phone": "الهاتف", "c_loc": "الموقع", "c_social": "تابعنا",
        "c_form": "أرسل رسالة", "c_name": "اسمك", "c_mail": "بريدك الإلكتروني", "c_msg": "رسالتك",
        "c_send": "أرسل عبر البريد", "c_hint": "سيفتح زر الإرسال تطبيق البريد لديك والرسالة جاهزة.",
        "c_subject": "رسالة من موقع Lumina CV",
        "c_empty": "بيانات التواصل ستتوفر قريبًا.",
        "ad_text": "رابط إعلاني: ادعم الموقع المجاني بزيارة راعينا",
        "ad_label": "إعلان",
        "view_edit": "✏️ تعديل نسخة من هذه السيرة",
        "view_note": "المحتوى من صاحب السيرة ولا يتحقق منه Lumina.",
        "f_about": "عن Lumina", "f_priv": "الخصوصية", "f_terms": "الشروط",
        "pg_updated": "آخر تحديث: نوفمبر 2026",
        "about_title": "عن Lumina CV",
        "about_secs": [
            ("ما هو Lumina CV", "أداة مجانية لصناعة سيرة ذاتية أنيقة بالعربية والإنجليزية: اختر القالب واللون، أدخل بياناتك، ثم احفظها PDF أو شاركها برابط."),
            ("لمن صُمم", "للخريجين وطالبي العمل الذين يريدون سيرة واضحة وسريعة دون تعقيد أو حساب. اختر القالب الكلاسيكي إن كانت الجهة تستخدم أنظمة فرز السير الذاتية."),
            ("مشروع مستقل", "Lumina CV مشروع مستقل صغير يتطور بحسب ملاحظات المستخدمين. اقتراحاتك مرحَّب بها عبر صفحة التواصل."),
        ],
        "privp_title": "سياسة الخصوصية",
        "privp_secs": [
            ("ما الذي تدخله", "البيانات التي تكتبها (الاسم ووسائل التواصل والخبرات وغيرها) تُستخدم فقط لبناء سيرتك داخل جلستك. لا نخزنها في قاعدة بيانات ولا نطلب منك إنشاء حساب."),
            ("روابط المشاركة", "عند إنشاء رابط للمشاركة تُضمَّن بيانات سيرتك داخل الرابط نفسه، ولا تُضاف صورتك الشخصية. أي شخص معه الرابط يستطيع قراءة ما فيه، فلا تشاركه إلا مع من تريد."),
            ("الملفات التي تحمّلها", "تُنشأ ملفات HTML وPDF من بيانات جلستك لحظة الطلب، ولا نحتفظ بنسخة منها."),
            ("أطراف خارجية", "يحمّل الموقع الخطوط من Google Fonts، ويُستضاف على Streamlit Community Cloud الذي قد يحتفظ بسجلات تقنية (مثل عنوان IP ونوع الجهاز) وفق سياسته الخاصة. الروابط الإعلانية وروابط الإحالة تنقلك إلى مواقع أخرى لها سياساتها. لا يحمّل الموقع أي سكربتات إعلانية."),
            ("ملفات تعريف الارتباط", "لا نضبط ملفات تعريف ارتباط للإعلانات أو التتبع. قد يستخدم Streamlit تقنيات جلسة لازمة لتشغيل التطبيق، وقد تضبط المواقع التي تزورها عبر الروابط الإعلانية ملفاتها الخاصة."),
            ("تواصل معنا", "لأي استفسار عن الخصوصية راسلنا على {email}."),
        ],
        "termsp_title": "شروط الاستخدام",
        "termsp_secs": [
            ("الخدمة", "Lumina CV أداة مجانية لإنشاء السير الذاتية، وتُقدَّم كما هي دون ضمانات من أي نوع، وقد تتغير أو تتوقف في أي وقت."),
            ("مسؤوليتك", "أنت المسؤول عن صحة المعلومات التي تضعها في سيرتك وعن استخدامها. لا نضمن حصولك على وظيفة أو قبولك لدى أي جهة."),
            ("الاستخدام المقبول", "لا تستخدم الموقع لنشر معلومات تخص غيرك دون إذنه أو لأي غرض غير قانوني."),
            ("الروابط والإعلانات", "قد يحتوي الموقع على روابط إعلانية أو روابط إحالة نحصل منها على عمولة دون تكلفة إضافية عليك، وتكون موسومة بوضوح. لسنا مسؤولين عن محتوى المواقع الخارجية."),
            ("التعديلات", "قد نحدّث هذه الشروط من وقت لآخر، واستمرارك في الاستخدام يعني موافقتك على النسخة المحدثة."),
        ],
        "dl_pdf": "تحميل PDF", "dl_html": "تحميل ملف HTML", "pdf_hint": "ستفتح نافذة الطباعة: اختر «حفظ كـ PDF» ثم احفظ الملف.",
        "support_line": "أعجبتك الأداة؟ ادعمنا برابط إعلاني (اختياري)",
        "res_title": "موارد مفيدة في رحلة البحث عن عمل",
        "res_note": "بعض هذه الروابط روابط إحالة: قد نحصل على عمولة دون أي تكلفة إضافية عليك.",
        "res_btn": "اعرف المزيد",
        "tools_title": "أدوات مجانية أخرى", "tools_btn": "افتح الأداة", "photo_tip": "الصورة كبيرة؟ صغّرها مجانًا بأداتنا لضغط الصور",
        "share_btn": "إنشاء رابط للمشاركة",
        "qr_check": "أضف رمز QR إلى سيرتي", "qr_label": "امسح لعرضها أونلاين", "qr_scan": "امسح الرمز لفتح سيرتك",
        "share_ready": "انسخ الرابط وأرسله للشركات.",
        "share_note": "سيرتك محفوظة داخل الرابط نفسه وليس على خادمنا. أي شخص معه الرابط يستطيع رؤيتها، والصورة الشخصية لا تُضاف إليه. اضغط الزر مرة أخرى بعد أي تعديل.",
        "share_long": "الرابط طويل جدًا وقد لا يفتح في كل مكان. اختصر بعض النصوص وحاول مجددًا.",
        "share_addr": "تم إنشاء الرابط. انسخه من شريط العنوان في المتصفح.",
        "view_made": "تم إنشاء هذه السيرة الذاتية مجانًا عبر Lumina CV",
        "view_cta": "اصنع سيرتك مجانًا",
        "photo_hint": "الصورة اختيارية.",
        "footer": "جميع الحقوق محفوظة", "footer2": "صُنع لمساعدتك على الحصول على الوظيفة",
        "demo": {
            "name": "أحمد سعيد", "title": "مهندس برمجيات متكامل", "email": "ahmed.said@email.com",
            "phone": "+20 100 123 4567", "city": "القاهرة، مصر",
            "links": "linkedin.com/in/ahmed-said\ngithub.com/ahmed-said",
            "summary": "مهندس برمجيات يسعى للنتائج، لديه خبرة واسعة في تصميم وبناء ونشر تطبيقات سحابية قوية وأنظمة مؤتمتة للشركات.",
            "exp": "مهندس برمجيات أول - نيكساتك (2022 - الآن)\nمطور برمجيات - كوانتم كود (2020 - 2022)",
            "edu": "بكالوريوس هندسة الحاسبات - جامعة القاهرة (امتياز / 2019)",
            "projects": "منصة حجوزات سحابية تخدم أكثر من 10 آلاف مستخدم\nأداة لأتمتة النشر المستمر للفرق الصغيرة",
            "courses": "شهادة AWS Solutions Architect\nدورة التصميم المعماري للأنظمة الموزعة",
            "skills": "بايثون, ريأكت, AWS, دوكر, SQL, جو",
            "langs": "العربية (اللغة الأم), الإنجليزية (متقدم)",
        },
    },
    "en": {
        "dir": "ltr", "ff": "'Plus Jakarta Sans','Segoe UI',sans-serif", "ffs": "'Source Serif 4',Georgia,serif",
        "nav": ["Home", "Builder", "Templates", "How it works", "Contact"],
        "lang_label": "Language",
        "hero_title": "Build a resume that gets noticed",
        "hero_sub": "Fill in your details, pick a template and color, and download a print-ready resume in minutes. Bilingual and completely free.",
        "cta_start": "Get started", "cta_tpl": "Browse templates",
        "prev_title": "This is how your resume will look",
        "feat_title": "Everything you need in one place",
        "features": [
            ("🌐", "Fully bilingual", "Every text switches with the language, and Arabic runs right-to-left automatically."),
            ("🎨", "Three templates, four colors", "Glass, classic and two-column. Change the look in one click."),
            ("🖼️", "Profile photo", "Upload your photo to show it in the resume and in the downloaded file."),
            ("🖨️", "Print and PDF ready", "A clean white file you can save as PDF from your browser."),
            ("🧩", "Complete sections", "Summary, experience, education, projects, courses, skills, languages and links."),
            ("🔒", "No account needed", "No sign-up and no database. Your data stays in your session only."),
        ],
        "steps_title": "Just three steps",
        "steps": [
            ("Fill in your details", "Type your information in the builder and watch the preview update."),
            ("Choose a design", "Pick the template and color that suit your field."),
            ("Download and print", "Download the file, then save it as PDF from your browser."),
        ],
        "b_title": "Resume Builder", "b_sub": "Edit your details on the side and see the result live.",
        "s_design": "Design", "tpl_label": "Template", "theme_label": "Color",
        "s_personal": "Personal details", "s_content": "Content", "s_extra": "Extra sections",
        "f_name": "Full name", "f_title": "Job title", "f_email": "Email address",
        "f_phone": "Phone number", "f_city": "City",
        "f_links": "Links (one per line)", "f_summary": "Professional summary",
        "f_exp": "Work experience (one job per line)", "f_edu": "Education & certifications (one per line)",
        "f_projects": "Projects (one per line)", "f_courses": "Courses (one per line)",
        "f_skills": "Skills (separate with commas)", "f_langs": "Languages (separate with commas)",
        "photo": "Upload your profile photo", "photo_ok": "Photo uploaded", "photo_rm": "Remove photo",
        "h_summary": "Professional Summary", "h_exp": "Work Experience", "h_edu": "Education & Certifications",
        "h_projects": "Projects", "h_courses": "Courses", "h_skills": "Skills", "h_langs": "Languages",
        "download": "Download resume", "tip": "Open the file, press Ctrl+P and choose Save as PDF.",
        "tpl_names": {"glass": "Glass", "classic": "Classic", "side": "Two-column"},
        "tpl_desc": {"glass": "A glowing dark look for the screen. It turns into clean white when downloaded.",
                     "classic": "A simple single column, the best fit for applicant tracking systems.",
                     "side": "A colored sidebar for contact and skills with the main content beside it."},
        "theme_names": ["Neon Cyan", "Royal Purple", "Luxury Gold", "Ocean Blue"],
        "t_title": "Templates", "t_sub": "Pick the design closest to your field. You can change it later.",
        "t_use": "Use this template", "t_cur": "Current template",
        "how_title": "How it works", "faq_title": "Frequently asked questions",
        "faqs": [
            ("Is it free?", "Yes, it is completely free and needs no account."),
            ("Is my data saved?", "Your data is never written to a database. It stays in your session while the page is open and disappears when you close or refresh it, so download your file before leaving."),
            ("How do I get a PDF?", "Download the file, open it in your browser, press Ctrl+P and choose Save as PDF."),
            ("Is my text translated when I switch language?", "No. Each language has its own fields, so write the Arabic and English versions separately."),
            ("Which photo formats are supported?", "PNG, JPG, JPEG and WebP."),
            ("Which template suits applicant tracking systems?", "The Classic template, because it is a single column of plain text with no complex elements."),
            ("Can I share my resume with a link?", "Yes. Click Create shareable link in the builder and copy it. Your data is stored inside the link itself, and anyone with the link can see it."),
        ],
        "priv_title": "Privacy", "priv_text": "We do not collect, sell or store your personal data in a database. The information you type is processed inside your session only to build your resume.",
        "terms_title": "Terms of use", "terms_text": "The service is provided as is. You are responsible for the accuracy of the information in your resume.",
        "c_title": "Contact us", "c_sub": "Have a suggestion or ran into a problem? Write to us.",
        "c_email": "Email", "c_phone": "Phone", "c_loc": "Location", "c_social": "Follow us",
        "c_form": "Send a message", "c_name": "Your name", "c_mail": "Your email", "c_msg": "Your message",
        "c_send": "Send by email", "c_hint": "The send button opens your email app with the message ready.",
        "c_subject": "Message from Lumina CV",
        "c_empty": "Contact details are coming soon.",
        "ad_text": "Sponsored link: support this free site by visiting our sponsor",
        "ad_label": "ADVERTISEMENT",
        "view_edit": "✏️ Edit a copy of this resume",
        "view_note": "Content is provided by the resume owner and is not verified by Lumina.",
        "f_about": "About Lumina", "f_priv": "Privacy", "f_terms": "Terms",
        "pg_updated": "Last updated: November 2026",
        "about_title": "About Lumina CV",
        "about_secs": [
            ("What is Lumina CV", "A free tool for building a clean resume in Arabic or English: pick a template and color, enter your details, then save it as a PDF or share it with a link."),
            ("Who it is for", "Graduates and job seekers who want a clear, fast resume without complexity or an account. Choose the Classic template if the employer uses applicant tracking systems."),
            ("An independent project", "Lumina CV is a small independent project that improves with user feedback. Suggestions are welcome through the Contact page."),
        ],
        "privp_title": "Privacy Policy",
        "privp_secs": [
            ("What you enter", "The details you type (name, contact info, experience and so on) are used only to build your resume inside your session. We do not store them in a database and we do not ask you to create an account."),
            ("Share links", "When you create a shareable link, your resume data is encoded inside the link itself, and your profile photo is not included. Anyone with the link can read it, so share it only with people you choose."),
            ("Files you download", "HTML and PDF files are generated from your session data at the moment you ask, and we do not keep a copy."),
            ("Third parties", "The site loads fonts from Google Fonts and is hosted on Streamlit Community Cloud, which may keep technical logs (such as IP address and device type) under its own policy. Sponsored and affiliate links take you to other sites with their own policies. The site does not load any advertising scripts."),
            ("Cookies", "We do not set advertising or tracking cookies. Streamlit may use session technology needed to run the app, and sites you visit through sponsored links may set their own cookies."),
            ("Contact", "For any privacy question, write to us at {email}."),
        ],
        "termsp_title": "Terms of Use",
        "termsp_secs": [
            ("The service", "Lumina CV is a free resume tool provided as is, without warranties of any kind, and it may change or stop at any time."),
            ("Your responsibility", "You are responsible for the accuracy of the information in your resume and how you use it. We do not guarantee that you will get a job or be accepted by any employer."),
            ("Acceptable use", "Do not use the site to publish information about other people without their permission, or for any unlawful purpose."),
            ("Links and advertising", "The site may contain sponsored or affiliate links that earn us a commission at no extra cost to you, and they are clearly labeled. We are not responsible for the content of external sites."),
            ("Changes", "We may update these terms from time to time, and continuing to use the site means you accept the updated version."),
        ],
        "dl_pdf": "Download PDF", "dl_html": "Download HTML file", "pdf_hint": "A print window opens: choose \"Save as PDF\" and save the file.",
        "support_line": "Liked the tool? Support us with a sponsored link (optional)",
        "res_title": "Helpful resources for your job search",
        "res_note": "Some of these are affiliate links: we may earn a commission at no extra cost to you.",
        "res_btn": "Learn more",
        "tools_title": "More free tools", "tools_btn": "Open tool", "photo_tip": "Photo too large? Shrink it free with our image compressor",
        "share_btn": "Create shareable link",
        "qr_check": "Add a QR code to my resume", "qr_label": "Scan to view online", "qr_scan": "Scan the code to open your resume",
        "share_ready": "Copy the link and send it to employers.",
        "share_note": "Your resume is stored inside the link itself, not on our server. Anyone with the link can see it, and your photo is not included. Click the button again after any edit.",
        "share_long": "This link is very long and may not open everywhere. Shorten some text and try again.",
        "share_addr": "Link created. Copy it from your browser's address bar.",
        "view_made": "This resume was created for free with Lumina CV",
        "view_cta": "Create yours for free",
        "photo_hint": "Photos are optional. Most US employers prefer resumes without one.",
        "footer": "All rights reserved", "footer2": "Built to help you land the job",
        "demo": {
            "name": "Alexander Wright", "title": "Senior Full-Stack Engineer", "email": "alex.wright@email.com",
            "phone": "+1 555 019 2834", "city": "New York, USA",
            "links": "linkedin.com/in/alex-wright\ngithub.com/alex-wright",
            "summary": "Results-driven full-stack engineer with extensive experience designing, building and deploying robust cloud applications and automated enterprise pipelines.",
            "exp": "Senior Full-Stack Engineer - NexaTech Solutions (2022 - Present)\nSoftware Developer - Quantum Code Systems (2020 - 2022)",
            "edu": "B.Sc. in Computer Engineering - MIT (GPA 3.9 / 2019)",
            "projects": "Cloud booking platform serving 10,000+ users\nContinuous deployment automation tool for small teams",
            "courses": "AWS Solutions Architect certification\nDistributed systems architecture course",
            "skills": "Python, React, AWS, Docker, SQL, Go",
            "langs": "English (Native), Arabic (Fluent)",
        },
    },
}

def encode_cv(d, tpl, th, lg):
    raw = json.dumps({"v": 1, "l": lg, "t": tpl, "h": th, "d": d}, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode().rstrip("=")


def decode_cv(tok):
    try:
        if not tok or len(tok) > 20000:
            return None
        raw = base64.urlsafe_b64decode(tok + "=" * (-len(tok) % 4))
        obj = json.loads(zlib.decompressobj().decompress(raw, 200000).decode("utf-8"))
        lg, tp, h, dd = obj["l"], obj["t"], int(obj["h"]), obj["d"]
        if lg not in T or tp not in TPLS or not 0 <= h < len(THEMES):
            return None
        return {"l": lg, "t": tp, "h": h, "d": {f: str(dd.get(f, ""))[:3000] for f in FIELDS}}
    except Exception:
        return None


def qr_uri(text):
    try:
        import io
        import segno
        buf = io.BytesIO()
        segno.make(text, error="l").save(buf, kind="svg", scale=4, border=3, dark="#111111", light="#ffffff",
                                         xmldecl=False, svgns=True, nl=False)
        svg = buf.getvalue().decode("utf-8").replace("<svg ", '<svg shape-rendering="crispEdges" ', 1)
        return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode()
    except Exception:
        return None


def base_url():
    try:
        u = st.context.url
        return u.split("?")[0].split("#")[0] if u else None
    except Exception:
        return None


# =====================================================================
# حالة الجلسة
# =====================================================================
for lg in T:
    for f in FIELDS:
        st.session_state.setdefault(f"{f}_{lg}", T[lg]["demo"][f])
st.session_state.setdefault("page", "home")
if "lang" not in st.session_state:
    try:
        _al = st.context.headers.get("Accept-Language", "")
    except Exception:
        _al = ""
    st.session_state.lang = "ar" if _al.lower().startswith("ar") else "en"
st.session_state.setdefault("tpl", "glass")
st.session_state.setdefault("th", 0)
st.session_state.setdefault("photo", None)
st.session_state.setdefault("photo_n", 0)
st.session_state.setdefault("view", None)
st.session_state.setdefault("qr_on", False)
_tin = st.query_params.get("cv")
if (_tin and not st.session_state.view and _tin != st.session_state.get("share_tok")
        and _tin != st.session_state.get("view_dismissed")):
    _v = decode_cv(_tin)
    if _v:
        st.session_state.view = _v
        st.session_state.lang, st.session_state.tpl, st.session_state.th = _v["l"], _v["t"], _v["h"]

# ستريمليت يمسح حالة الحقول اللي مش معروضة، فبنثبتها هنا
for _lg in T:
    for _f in FIELDS:
        st.session_state[f"{_f}_{_lg}"] = st.session_state[f"{_f}_{_lg}"]
for _k in ("page", "lang", "tpl", "th", "qr_on"):
    st.session_state[_k] = st.session_state[_k]

lang = st.session_state.lang
L = T[lang]
TH = THEMES[st.session_state.th]


def go(page, tpl=None):
    st.session_state.page = page
    if tpl:
        st.session_state.tpl = tpl


def exit_view():
    st.session_state.view_dismissed = st.query_params.get("cv")
    st.session_state.view = None
    st.query_params.clear()
    st.session_state.page = "builder"


def edit_copy():
    v = st.session_state.view
    if v:
        for f in FIELDS:
            st.session_state[f"{f}_{v['l']}"] = v["d"][f]
        st.session_state.lang, st.session_state.tpl, st.session_state.th = v["l"], v["t"], v["h"]
    st.session_state.view_dismissed = st.query_params.get("cv")
    st.session_state.view = None
    st.query_params.clear()
    st.session_state.page = "builder"


def toggle_lang():
    st.session_state.lang = "en" if st.session_state.lang == "ar" else "ar"


def remove_photo():
    st.session_state.photo = None
    st.session_state.photo_n += 1


def md(s):
    st.markdown(" ".join(s.split()), unsafe_allow_html=True)


# =====================================================================
# CSS الخاص بالسيرة (مشترك بين المعاينة وملف التحميل)
# =====================================================================
CV_CSS = """
.cvx{--ff:inherit;font-family:var(--ff);line-height:1.75;border-radius:22px;overflow:hidden;color:var(--tx);padding:36px;text-align:start}
.cvx *{box-sizing:border-box}
.cvx h2,.cvx h3,.cvx h4,.cvx p{margin:0;padding:0}
.cvx.dark{--bg:rgba(255,255,255,.06);--tx:#eef2ff;--mu:#b9c3de;--cd:rgba(255,255,255,.07);--bd:rgba(255,255,255,.14);--hd:#fff;--ac:var(--a)}
.cvx.paper{--bg:#fff;--tx:#1f2430;--mu:#5b6475;--cd:#f3f5fa;--bd:#e3e7f0;--hd:#111827;--ac:var(--b)}
.cvx .hd{display:flex;gap:26px;align-items:center;flex-wrap:wrap;padding-bottom:22px;border-bottom:1px solid var(--bd)}
.cvx .av{width:140px;height:140px;border-radius:50%;object-fit:cover;flex:none}
.cvx img.av{padding:4px;background:linear-gradient(135deg,var(--a),var(--b))}
.cvx .av.ph{display:flex;align-items:center;justify-content:center;font-size:2.8rem;font-weight:800;color:#fff;background:linear-gradient(135deg,var(--a),var(--b))}
.cvx h2{font-size:2.1rem;font-weight:800;color:var(--hd);line-height:1.25}
.cvx h3{font-size:1.15rem;font-weight:600;color:var(--ac);margin:4px 0 10px}
.cvx .ct{display:flex;flex-wrap:wrap;gap:6px 18px;color:var(--mu);font-size:.93rem}
.cvx .lk{display:flex;flex-wrap:wrap;gap:6px 14px;margin-top:6px;font-size:.9rem}
.cvx .lk a{color:var(--ac);text-decoration:none;border-bottom:1px dotted currentColor}
.cvx .sc{margin-top:26px}
.cvx .sc h4{font-size:1.1rem;font-weight:700;color:var(--hd);padding-bottom:7px;margin-bottom:12px;border-bottom:2px solid color-mix(in srgb,var(--ac) 65%,transparent)}
.cvx .sc p{color:var(--tx)}
.cvx .qrb{display:flex;justify-content:flex-end;margin-top:30px}
.cvx .qr{display:flex;flex-direction:column;align-items:center;gap:6px;font-size:.78rem;color:var(--mu);text-align:center}
.cvx .qr img{width:240px;height:240px;max-width:100%;background:#fff;border-radius:10px;padding:4px;border:1px solid var(--bd)}
.cvx .it{background:var(--cd);border-radius:12px;padding:10px 16px;margin-bottom:8px}
.cvx .ch{display:inline-block;margin:3px;padding:5px 14px;border-radius:999px;font-weight:600;font-size:.88rem;color:var(--hd);background:color-mix(in srgb,var(--a) 18%,transparent);border:1px solid color-mix(in srgb,var(--ac) 50%,transparent)}
.t-glass{background:var(--bg);backdrop-filter:blur(14px);border:1px solid var(--bd)}
.t-glass.dark{box-shadow:0 0 60px color-mix(in srgb,var(--a) 22%,transparent)}
.t-glass.dark .av{box-shadow:0 0 28px color-mix(in srgb,var(--a) 70%,transparent)}
.t-glass .it{border-inline-start:3px solid var(--a)}
.t-classic{background:#fff;padding:44px;border-radius:8px;border-top:8px solid var(--b)}
.t-classic .hd{border-bottom:2px solid var(--hd)}
.t-classic .av{border-radius:12px}
.t-classic .it{background:none;border-radius:0;padding:2px 0;margin-bottom:4px}
.t-classic .it::before{content:"▪ ";color:var(--ac)}
.t-classic .ch{background:none;border-radius:6px}
.t-side{display:grid;grid-template-columns:minmax(0,34fr) minmax(0,66fr);padding:0;background:#fff}
.t-side aside{background:linear-gradient(160deg,color-mix(in srgb,var(--b) 75%,#111),color-mix(in srgb,var(--b) 45%,#111));color:#fff;padding:32px 22px}
.t-side aside .av{width:130px;height:130px;margin:0 auto 18px;display:flex}
.t-side aside .sc h4{color:#fff;border-color:rgba(255,255,255,.4);font-size:1rem}
.t-side aside .ct{flex-direction:column;color:#f4f4f4}
.t-side aside .lk a{color:#fff}
.t-side aside .ch{color:#fff;background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.35)}
.t-side main{padding:34px 30px;display:block}
.t-side main .id h2{margin-bottom:2px}
@media(max-width:700px){.cvx{padding:22px}.t-classic{padding:24px}.t-side{grid-template-columns:1fr}}
@media print{.cvx{box-shadow:none!important}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
"""


def lines(text):
    return [x.strip().lstrip("•-–▪ ").strip() for x in text.splitlines() if x.strip()]


def csv(text):
    return [x.strip() for x in text.replace("،", ",").split(",") if x.strip()]


def cv_html(d, tpl, theme, photo=None, paper=False, qr=None):
    e = html.escape
    name = d["name"].strip()
    initials = "".join(w[0] for w in name.split()[:2]).upper() or "CV"
    if photo:
        av = f'<img class="av" alt="" src="data:{photo[0]};base64,{base64.b64encode(photo[1]).decode()}"/>'
    else:
        av = f'<div class="av ph">{e(initials)}</div>'

    ct = "".join(f"<span>{i} {e(v.strip())}</span>"
                 for i, v in (("✉️", d["email"]), ("📱", d["phone"]), ("📍", d["city"])) if v.strip())
    lk_items = []
    for u in lines(d["links"]):
        href = u if u.startswith("http") else "https://" + u
        shown = u.replace("https://", "").replace("http://", "").rstrip("/")
        lk_items.append(f'<a href="{e(href, quote=True)}" target="_blank" rel="noopener noreferrer nofollow ugc">{e(shown)}</a>')
    lk = f'<div class="lk">{"".join(lk_items)}</div>' if lk_items else ""

    def sec(icon, key, body):
        return f'<div class="sc"><h4>{icon} {e(L[key])}</h4>{body}</div>' if body else ""

    def its(arr):
        return "".join(f'<div class="it">{e(x)}</div>' for x in arr)

    def chips(arr):
        return "".join(f'<span class="ch">{e(x)}</span>' for x in arr)

    summary = f"<p>{e(d['summary'].strip())}</p>" if d["summary"].strip() else ""
    s_sum = sec("🎯", "h_summary", summary)
    s_exp = sec("💼", "h_exp", its(lines(d["exp"])))
    s_edu = sec("🎓", "h_edu", its(lines(d["edu"])))
    s_pro = sec("🚀", "h_projects", its(lines(d["projects"])))
    s_cou = sec("📜", "h_courses", its(lines(d["courses"])))
    s_ski = sec("⚡", "h_skills", chips(csv(d["skills"])))
    s_lan = sec("🌍", "h_langs", chips(csv(d["langs"])))

    qr_html = f'<div class="qr"><img src="{qr}" alt="QR"/><span>{e(L["qr_label"])}</span></div>' if qr else ""
    qr_bar = f'<div class="qrb">{qr_html}</div>' if qr_html else ""
    cls = "paper" if (paper or tpl != "glass") else "dark"
    ff = L["ffs"] if tpl == "classic" else L["ff"]
    style = f'--a:{theme["a"]};--b:{theme["b"]};--ff:{ff};'
    ident = f'<div class="id"><h2>{e(name)}</h2><h3>{e(d["title"].strip())}</h3></div>'

    if tpl == "side":
        body = (f'<aside>{av}<div class="sc"><div class="ct">{ct}</div>{lk}</div>{s_ski}{s_lan}</aside>'
                f'<main>{ident}{s_sum}{s_exp}{s_edu}{s_pro}{s_cou}{qr_bar}</main>')
    else:
        head = f'<div class="hd">{av}<div class="id"><h2>{e(name)}</h2><h3>{e(d["title"].strip())}</h3><div class="ct">{ct}</div>{lk}</div></div>'
        body = f'{head}{s_sum}{s_exp}{s_edu}{s_pro}{s_cou}{s_ski}{s_lan}{qr_bar}'
    return f'<div class="cvx t-{tpl} {cls}" dir="{L["dir"]}" style="{style}">{body}</div>'


def download_doc(d, tpl, theme, photo, qr=None):
    body = cv_html(d, tpl, theme, photo, paper=True, qr=qr)
    return f"""<!DOCTYPE html><html lang="{lang}" dir="{L['dir']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(d['name'])} - {'Resume' if lang == 'en' else 'CV'}</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600;800&family=Source+Serif+4:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{{margin:0;padding:24px;background:#fff}}.wrap{{max-width:860px;margin:auto}}{CV_CSS}
@page{{size:{'letter' if lang == 'en' else 'A4'};margin:6mm}}
@media print{{
  html,body{{padding:0!important;margin:0!important;background:#fff}}
  .wrap{{max-width:100%!important;zoom:0.90}}
  .cvx{{padding:18px 22px!important;border-radius:0!important;box-shadow:none!important}}
  .cvx .sc{{margin-top:10px!important}}
  .cvx .sc h4{{margin-bottom:6px!important;break-after:avoid}}
  .cvx .it{{margin-bottom:5px!important;padding:6px 10px!important;break-inside:avoid}}
  .cvx .qr{{break-inside:avoid}}
}}</style></head><body><div class="wrap">{body}</div></body></html>"""


def pdf_button(d, tpl, theme, photo, qr, label):
    """زر PDF: يطبع السيرة الذاتية في صفحة واحدة تلقائياً على الموبايل والكمبيوتر."""
    try:
        raw_title = f"{d['name'].strip() or 'CV'} - {'Resume' if lang == 'en' else 'CV'}"
        js_title = json.dumps(raw_title).replace("<", "\\u003c").replace(">", "\\u003e")
        page = "letter" if lang == "en" else "A4"
        doc = f"""<!DOCTYPE html><html lang="{lang}" dir="{L['dir']}"><head><meta charset="utf-8"><title>{html.escape(raw_title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600;800&family=Source+Serif+4:wght@400;600;700&display=swap" rel="stylesheet">
<style>html,body{{margin:0;background:transparent;font-family:{L['ff']}}}
.btn{{width:100%;height:48px;border:0;border-radius:14px;color:#fff;font-weight:700;font-size:1rem;cursor:pointer;font-family:inherit;background:linear-gradient(135deg,{theme['a']},{theme['b']})}}
.btn:hover{{filter:brightness(1.08)}}
.sheet{{position:absolute;left:-99999px;top:0;width:860px}}
{CV_CSS}
@page{{size:{page};margin:6mm}}
@media print{{
  .btn{{display:none!important}}
  html,body{{background:#fff;margin:0!important;padding:0!important}}
  .sheet{{position:static;width:auto;zoom:0.90}}
  .cvx{{border-radius:0!important;padding:18px 22px!important;box-shadow:none!important;line-height:1.4!important}}
  .cvx .sc{{margin-top:10px!important}}
  .cvx .sc h4{{margin-bottom:6px!important;break-after:avoid}}
  .cvx .it{{margin-bottom:5px!important;padding:6px 10px!important;break-inside:avoid}}
  .cvx .qr{{break-inside:avoid}}
  .t-side{{grid-template-columns:minmax(0,34fr) minmax(0,66fr)!important}}
}}</style></head><body>
<button class="btn" onclick="go()">{html.escape(label)}</button>
<div class="sheet" id="printSheet">{cv_html(d, tpl, theme, photo, paper=True, qr=qr)}</div>
<script>function go(){{var T={js_title},old=null;try{{old=window.parent.document.title;window.parent.document.title=T;}}catch(e){{}}
var f=(document.fonts&&document.fonts.ready)?document.fonts.ready:Promise.resolve();
f.then(function(){{window.print();try{{if(old!==null)window.parent.document.title=old;}}catch(e){{}}}});}}</script></body></html>"""
        if hasattr(st, "iframe"):
            st.iframe(doc, height=56)
        else:
            import streamlit.components.v1 as components
            components.html(doc, height=56)
    except Exception:
        pass


def current_data():
    return {f: st.session_state[f"{f}_{lang}"] for f in FIELDS}


# =====================================================================
# CSS الموقع
# =====================================================================
A, B, BG = TH["a"], TH["b"], TH["bg"]
align = "right" if L["dir"] == "rtl" else "left"
SITE_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&family=Plus+Jakarta+Sans:wght@400;600;800&family=Source+Serif+4:wght@400;600;700&display=swap');
:root{{--a:{A};--b:{B};}}
.stApp{{background:radial-gradient(circle at 12% 8%,color-mix(in srgb,{B} 30%,transparent),transparent 42%),radial-gradient(circle at 88% 92%,color-mix(in srgb,{A} 20%,transparent),transparent 42%),{BG};color:#e8ecfa}}
.stApp,.stApp p,.stApp li,.stApp label,.stApp input,.stApp textarea,.stApp button,.stApp summary{{font-family:{L['ff']}}}
.stApp [data-testid="stIconMaterial"],.stApp [class*="material-icons"],.stApp [class*="material-symbols"]{{font-family:'Material Symbols Rounded','Material Icons'!important;font-style:normal;font-weight:400;letter-spacing:normal;text-transform:none;white-space:nowrap;direction:ltr;-webkit-font-feature-settings:'liga';font-feature-settings:'liga'}}
.stApp [data-testid="stWidgetLabel"] *,.stApp label p,.stApp li,.stApp .stMarkdown p{{color:#d5dcf2}}
.stApp [data-testid="stAppViewContainer"],.stApp [data-testid="stMain"]{{direction:{L['dir']}}}
header[data-testid="stHeader"],#MainMenu,footer,[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{{display:none!important}}
.block-container{{max-width:1180px;padding-top:1.2rem;padding-bottom:2rem}}
.stTextInput input,.stTextArea textarea{{background:rgba(255,255,255,.06)!important;color:#fff!important;border:1px solid rgba(255,255,255,.18)!important;border-radius:12px!important;text-align:start}}
.stSelectbox div[data-baseweb="select"]>div{{background:rgba(255,255,255,.06)!important;border:1px solid rgba(255,255,255,.18)!important;border-radius:12px!important}}
.stSelectbox div[data-baseweb="select"] *{{color:#fff!important}}
/* Streamlit الجديد شال data-baseweb، فبنستهدف الـ data-testid الثابتة لحقول الكتابة */
[data-testid="stTextInputRootElement"],[data-testid="stTextAreaRootElement"]{{background:rgba(255,255,255,.08)!important;border:1px solid rgba(255,255,255,.2)!important;border-radius:12px!important}}
[data-testid="stTextInputRootElement"]:focus-within,[data-testid="stTextAreaRootElement"]:focus-within{{border-color:{A}!important;box-shadow:0 0 0 1px {A}!important}}
[data-testid="stTextInputRootElement"] *,[data-testid="stTextAreaRootElement"] *{{background-color:transparent!important}}
[data-testid="stTextInputField"],[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stTextAreaRootElement"] textarea{{color:#fff!important;-webkit-text-fill-color:#fff!important;caret-color:#fff!important;background:transparent!important}}
[data-testid="stTextInputField"]::placeholder,[data-testid="stTextArea"] textarea::placeholder{{color:#8c97b8!important;-webkit-text-fill-color:#8c97b8!important;opacity:1}}
/* إجبار الوضع الداكن على كل الأجهزة (الموبايل في الوضع الفاتح كان بيخلي الحقول بيضا والكتابة بيضا) */
:root{{color-scheme:dark}}
.stApp div[data-baseweb="input"],.stApp div[data-baseweb="base-input"],.stApp div[data-baseweb="textarea"]{{background:rgba(255,255,255,.07)!important;border-radius:12px!important}}
.stApp div[data-baseweb="input"],.stApp div[data-baseweb="textarea"]{{border:1px solid rgba(255,255,255,.18)!important}}
.stTextInput input,.stTextArea textarea{{background:transparent!important;color:#fff!important;-webkit-text-fill-color:#fff!important;caret-color:#fff}}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{{color:#8c97b8!important;-webkit-text-fill-color:#8c97b8!important}}
.stSelectbox div[data-baseweb="select"]>div{{background:rgba(255,255,255,.07)!important}}
.stSelectbox svg{{fill:#d5dcf2!important}}
div[data-baseweb="popover"] ul,div[data-baseweb="popover"] [role="listbox"]{{background:#161b2b!important}}
div[data-baseweb="popover"] li,div[data-baseweb="popover"] [role="option"]{{background:#161b2b!important;color:#e8ecfa!important}}
div[data-baseweb="popover"] li:hover,div[data-baseweb="popover"] [aria-selected="true"]{{background:#26304a!important}}
[data-testid="stExpander"] details,[data-testid="stExpander"] summary{{background:transparent!important}}
[data-testid="stAlert"]{{background:rgba(255,255,255,.07)!important;border:1px solid rgba(255,255,255,.15)}}
[data-testid="stAlert"] *{{color:#e8ecfa!important}}
[data-testid="stCode"] pre{{background:#0f1424!important}}
[data-testid="stCode"] *{{color:#cfe8ff!important}}
[data-testid="stCaptionContainer"] *{{color:#aab4cf!important}}
[data-testid="stExpander"]{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12)!important;border-radius:16px;margin-bottom:12px}}
[data-testid="stExpander"] summary,[data-testid="stExpander"] summary *{{color:#fff!important;font-weight:700}}
[data-testid="stFileUploader"] section{{background:rgba(255,255,255,.05);border:1px dashed rgba(255,255,255,.25);border-radius:14px}}
[data-testid="stFileUploader"] section *{{color:#d5dcf2!important}}
.stButton button,.stDownloadButton button{{background:rgba(255,255,255,.07)!important;color:#e8ecfa!important;border:1px solid rgba(255,255,255,.18)!important;border-radius:14px!important;font-weight:600;transition:transform .2s,box-shadow .2s}}
.stButton button[kind="primary"],.stButton button[data-testid="stBaseButton-primary"],.stDownloadButton button[kind="primary"],.stDownloadButton button[data-testid="stBaseButton-primary"],.stLinkButton a{{background:linear-gradient(135deg,{A},{B})!important;color:#fff!important;border:0!important;font-weight:700;padding:.65rem 1.2rem;border-radius:14px!important}}
.stButton button *,.stDownloadButton button *,.stLinkButton a *{{color:inherit!important}}
.stButton button:hover,.stDownloadButton button:hover,.stLinkButton a:hover{{transform:translateY(-2px);box-shadow:0 8px 28px color-mix(in srgb,{B} 55%,transparent)}}
.st-key-topnav .stButton button{{padding:.5rem .4rem;white-space:nowrap;font-size:.92rem}}
@media(max-width:768px){{
.st-key-topnav [data-testid="stHorizontalBlock"]{{flex-wrap:wrap!important;gap:6px!important}}
.st-key-topnav [data-testid="stColumn"]{{width:auto!important;min-width:0!important;flex:1 1 auto!important}}
.st-key-topnav [data-testid="stColumn"]:first-child{{flex:1 1 100%!important}}
.st-key-topnav .stButton button{{min-height:2.1rem;padding:.3rem .6rem;font-size:.85rem}}
.block-container{{padding-left:1rem;padding-right:1rem}}
}}
.st-key-viewtop{{direction:ltr}}
.st-key-viewtop [data-testid="stHorizontalBlock"]{{flex-wrap:nowrap!important;gap:10px!important}}
.st-key-viewtop [data-testid="stColumn"]{{min-width:0!important}}
.st-key-viewtop .stButton button{{padding:.4rem .6rem;font-size:.88rem;white-space:nowrap}}
.stRadio [role="radiogroup"]{{gap:6px;flex-wrap:wrap}}
.stRadio label[data-baseweb="radio"]{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:6px 16px;margin:0;cursor:pointer}}
.stRadio label[data-baseweb="radio"]>div:first-child{{display:none}}
.stRadio label[data-baseweb="radio"]:has(input:checked){{background:linear-gradient(135deg,{A},{B});border-color:transparent}}
.stRadio label[data-baseweb="radio"]:has(input:checked) *{{color:#fff!important;font-weight:700}}
.brand{{font-size:1.5rem;font-weight:800;background:linear-gradient(90deg,{A},{B});-webkit-background-clip:text;-webkit-text-fill-color:transparent;padding-top:4px}}
.hero{{text-align:center;padding:56px 10px 18px}}
.hero h1{{font-size:clamp(2rem,5vw,3.6rem);font-weight:800;line-height:1.25;margin:0 0 14px;background:linear-gradient(90deg,{A},{B},{A});background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shine 5s linear infinite}}
@keyframes shine{{to{{background-position:200% center}}}}
@media(prefers-reduced-motion:reduce){{.hero h1{{animation:none}}}}
.hero p{{max-width:640px;margin:0 auto;color:#aab4cf;font-size:1.1rem;line-height:1.9}}
.ptitle{{font-size:2rem;font-weight:800;color:#fff;margin:6px 0 4px}}
.psub{{color:#aab4cf;margin-bottom:18px}}
.h2s{{font-size:1.6rem;font-weight:800;color:#fff;text-align:center;margin:46px 0 20px}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}}
.fc{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:22px;backdrop-filter:blur(10px)}}
.fc .ic{{font-size:1.8rem}}
.fc h5{{font-size:1.05rem;font-weight:700;color:#fff;margin:8px 0 6px}}
.fc p,.fc a{{color:#b9c3de;font-size:.95rem;line-height:1.8;margin:0;text-decoration:none;word-break:break-word}}
.fc a:hover{{color:{A}}}
.stp{{display:flex;gap:14px;align-items:flex-start}}
.stp .n{{flex:none;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;background:linear-gradient(135deg,{A},{B})}}
.thumb{{height:440px;overflow:hidden;border-radius:18px;margin-bottom:12px;pointer-events:none;background:rgba(255,255,255,.03)}}
.thumb .cvx{{zoom:.4;width:250%}}
.tname{{font-weight:800;color:#fff;font-size:1.1rem}}
.tdesc{{color:#b9c3de;font-size:.92rem;min-height:70px}}
.foot{{text-align:center;color:#8c97b8;font-size:.88rem;border-top:1px solid rgba(255,255,255,.1);margin-top:50px;padding-top:20px;line-height:1.9}}
.foot b{{color:#fff}}
.spons{{display:inline-block;margin-top:10px;padding:6px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.2);color:#cfd6ee!important;text-decoration:none;font-size:.82rem}}
.supp{{font-size:.85rem;margin:6px 0 12px}}
.supp a{{color:#aab4cf;text-decoration:none;border-bottom:1px dotted #aab4cf}}
.adslot{{margin:34px auto 10px;text-align:center}}
.adlbl{{font-size:.7rem;letter-spacing:.14em;color:#8c97b8;margin-bottom:8px}}
.spons:hover{{border-color:{A}}}
{CV_CSS}
"""
md(f"<style>{SITE_CSS}</style>")


def support_html():
    if not AD_LINK:
        return ""
    return (f'<div class="supp">📢 <a href="{html.escape(AD_LINK, quote=True)}" target="_blank" '
            f'rel="noopener sponsored nofollow">{html.escape(L["support_line"])}</a></div>')


def ad_slot():
    b = AD_BANNER
    if not (b.get("img") and b.get("url")):
        return ""
    w = int(b.get("width", 300))
    return (f'<div class="adslot"><div class="adlbl">{html.escape(L["ad_label"])}</div>'
            f'<a href="{html.escape(b["url"], quote=True)}" target="_blank" rel="noopener sponsored nofollow">'
            f'<img src="{html.escape(b["img"], quote=True)}" alt="{html.escape(b.get("alt", "Advertisement"), quote=True)}" '
            f'loading="lazy" style="width:{w}px;max-width:100%;border-radius:10px;display:block;margin:auto"/></a></div>')


def tools_html():
    items = [t for t in OTHER_TOOLS if t.get("url")]
    if not items:
        return ""
    cards = "".join(
        f'<div class="fc"><div class="ic">{html.escape(t.get("icon", "🛠️"))}</div><h5>{html.escape(t["title"][lang])}</h5>'
        f'<p>{html.escape(t["desc"][lang])}</p><p style="margin-top:10px"><a href="{html.escape(t["url"], quote=True)}" '
        f'target="_blank" rel="noopener">{html.escape(L["tools_btn"])} ←</a></p></div>' for t in items)
    return f'<div class="h2s">{html.escape(L["tools_title"])}</div><div class="grid3">{cards}</div>'


def compress_photo(data, mime):
    try:
        import io
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(io.BytesIO(data)))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((520, 520))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=85, optimize=True)
        return "image/jpeg", buf.getvalue()
    except Exception:
        return mime, data


def resources_html():
    items = [a for a in AFFILIATES if a.get("url")]
    if not items:
        return ""
    cards = "".join(
        f'<div class="fc"><h5>{html.escape(a["title"][lang])}</h5><p>{html.escape(a["desc"][lang])}</p>'
        f'<p style="margin-top:10px"><a href="{html.escape(a["url"], quote=True)}" target="_blank" '
        f'rel="noopener sponsored nofollow">{html.escape(L["res_btn"])} ←</a></p></div>' for a in items)
    return (f'<div class="h2s">{html.escape(L["res_title"])}</div><div class="grid3">{cards}</div>'
            f'<div class="psub" style="text-align:center;margin-top:12px;font-size:.85rem">{html.escape(L["res_note"])}</div>')

# =====================================================================
# الهيدر: الشعار + التنقل + اللغة
# =====================================================================
if st.session_state.view:
    _v = st.session_state.view
    with st.container(key="viewtop"):
        _bc, _cc = st.columns([3, 2], vertical_alignment="center")
        _bc.markdown('<div class="brand">✨ Lumina CV</div>', unsafe_allow_html=True)
        _cc.button(L["view_cta"], on_click=exit_view, type="primary", use_container_width=True, key="view_cta")
    md(f'<div style="max-width:880px;margin:18px auto">{cv_html(_v["d"], _v["t"], THEMES[_v["h"]])}</div>')
    _, _mid, _ = st.columns([1, 2, 1])
    with _mid:
        pdf_button(_v["d"], _v["t"], THEMES[_v["h"]], None, None, "⬇️ " + L["dl_pdf"])
        st.caption(L["pdf_hint"])
        st.button(L["view_edit"], on_click=edit_copy, use_container_width=True, key="view_edit")
        st.download_button("📄 " + L["dl_html"], use_container_width=True,
                           data=download_doc(_v["d"], _v["t"], THEMES[_v["h"]], None).encode("utf-8"),
                           file_name=f"{'Resume' if lang == 'en' else 'CV'}_{_v['d']['name'].strip().replace(' ', '_') or 'CV'}.html",
                           mime="text/html")
    md(f'<div class="foot"><b>✨ Lumina CV</b><br>{html.escape(L["view_made"])}<br><span style="font-size:.78rem">{html.escape(L["view_note"])}</span></div>')
    st.stop()

page = st.session_state.page
with st.container(key="topnav"):
    _cols = st.columns([2.4, 1.1, 1.3, 1.1, 1.4, 1.1, 1.1], vertical_alignment="center")
    with _cols[0]:
        md('<div class="brand">✨ Lumina CV</div>')
    for _c, _p in zip(_cols[1:6], PAGES):
        _c.button(L["nav"][PAGES.index(_p)], key=f"nav_{_p}", on_click=go, args=(_p,),
                  type="primary" if page == _p else "secondary", use_container_width=True)
    _cols[6].button("English" if lang == "ar" else "العربية", key="lang_btn", on_click=toggle_lang, use_container_width=True)
demo = L["demo"]
photo = st.session_state.photo

# =====================================================================
# الرئيسية
# =====================================================================
if page == "home":
    md(f'<div class="hero"><h1>✨ {html.escape(L["hero_title"])}</h1><p>{html.escape(L["hero_sub"])}</p></div>')
    _, c1, c2, _ = st.columns([3, 2, 2, 3])
    c1.button(L["cta_start"], on_click=go, args=("builder",), use_container_width=True, key="h_start", type="primary")
    c2.button(L["cta_tpl"], on_click=go, args=("templates",), use_container_width=True, key="h_tpl", type="primary")

    md(f'<div class="h2s">{html.escape(L["prev_title"])}</div>')
    md(f'<div style="max-width:880px;margin:auto">{cv_html(demo, "glass", TH)}</div>')
    md(ad_slot())

    md(f'<div class="h2s">{html.escape(L["feat_title"])}</div>')
    cards = "".join(f'<div class="fc"><div class="ic">{i}</div><h5>{html.escape(t)}</h5><p>{html.escape(x)}</p></div>'
                    for i, t, x in L["features"])
    md(f'<div class="grid3">{cards}</div>')

    md(f'<div class="h2s">{html.escape(L["steps_title"])}</div>')
    steps = "".join(f'<div class="fc stp"><div class="n">{n}</div><div><h5 style="margin-top:0">{html.escape(t)}</h5><p>{html.escape(x)}</p></div></div>'
                    for n, (t, x) in enumerate(L["steps"], 1))
    md(f'<div class="grid3">{steps}</div>')
    md(tools_html())
    md(resources_html())

# =====================================================================
# المنشئ
# =====================================================================
elif page == "builder":
    md(f'<div class="ptitle">{html.escape(L["b_title"])}</div><div class="psub">{html.escape(L["b_sub"])}</div>')
    form, prev = st.columns([5, 6], gap="large")

    with form:
        with st.expander("🎨 " + L["s_design"], expanded=True):
            st.selectbox(L["tpl_label"], TPLS, key="tpl", format_func=lambda x: L["tpl_names"][x])
            st.selectbox(L["theme_label"], range(len(THEMES)), key="th", format_func=lambda i: L["theme_names"][i])
        with st.expander("📝 " + L["s_personal"], expanded=True):
            st.text_input(L["f_name"], key=f"name_{lang}")
            st.text_input(L["f_title"], key=f"title_{lang}")
            st.text_input(L["f_email"], key=f"email_{lang}")
            st.text_input(L["f_phone"], key=f"phone_{lang}")
            st.text_input(L["f_city"], key=f"city_{lang}")
            st.text_area(L["f_links"], key=f"links_{lang}", height=80)
            st.caption(L["photo_hint"])
            _tl = next((t["url"] for t in OTHER_TOOLS if t.get("url")), None)
            if _tl:
                md(f'<div class="supp">🖼️ <a href="{html.escape(_tl, quote=True)}" target="_blank" rel="noopener">{html.escape(L["photo_tip"])}</a></div>')
            up = st.file_uploader(L["photo"], type=["png", "jpg", "jpeg", "webp"], key=f"pu_{st.session_state.photo_n}")
            if up is not None:
                _fid = getattr(up, "file_id", None) or f"{up.name}-{up.size}"
                if st.session_state.get("photo_fid") != _fid:
                    st.session_state.photo = compress_photo(up.getvalue(), up.type or "image/png")
                    st.session_state.photo_fid = _fid
                photo = st.session_state.photo
            if st.session_state.photo:
                st.caption("✅ " + L["photo_ok"])
                st.button(L["photo_rm"], on_click=remove_photo, key="rm_photo")
        with st.expander("💼 " + L["s_content"], expanded=True):
            st.text_area(L["f_summary"], key=f"summary_{lang}", height=120)
            st.text_area(L["f_exp"], key=f"exp_{lang}", height=130)
            st.text_area(L["f_edu"], key=f"edu_{lang}", height=90)
            st.text_input(L["f_skills"], key=f"skills_{lang}")
        with st.expander("🧩 " + L["s_extra"], expanded=False):
            st.text_area(L["f_projects"], key=f"projects_{lang}", height=100)
            st.text_area(L["f_courses"], key=f"courses_{lang}", height=100)
            st.text_input(L["f_langs"], key=f"langs_{lang}")

    with prev:
        d = current_data()
        _qr = st.session_state.get("share_qr") if st.session_state.qr_on else None
        pdf_button(d, st.session_state.tpl, TH, photo, _qr, "⬇️ " + L["dl_pdf"])
        st.caption(L["pdf_hint"])
        st.download_button("📄 " + L["dl_html"],
                           data=download_doc(d, st.session_state.tpl, TH, photo, _qr).encode("utf-8"),
                           file_name=f"{'Resume' if lang == 'en' else 'CV'}_{d['name'].strip().replace(' ', '_') or 'CV'}.html",
                           mime="text/html", use_container_width=True)
        md(support_html())
        if st.button("🔗 " + L["share_btn"], key="share_btn", use_container_width=True):
            _t = encode_cv(d, st.session_state.tpl, st.session_state.th, lang)
            st.session_state.share_tok = _t
            st.query_params["cv"] = _t
            _b = base_url()
            st.session_state.share_link = f"{_b}?cv={_t}" if _b and len(_t) <= 6000 else None
            st.session_state.share_qr = qr_uri(st.session_state.share_link) if st.session_state.share_link else None
        _tok = st.session_state.get("share_tok")
        if _tok:
            if len(_tok) > 6000:
                st.warning(L["share_long"])
            elif st.session_state.get("share_link"):
                st.caption(L["share_ready"])
                st.code(st.session_state.share_link, language=None)
                if st.session_state.get("share_qr"):
                    md(f'<div style="text-align:center"><img src="{st.session_state.share_qr}" alt="QR" style="width:240px;height:240px;background:#fff;border-radius:12px;padding:4px"/><div style="color:#aab4cf;font-size:.85rem">{html.escape(L["qr_scan"])}</div></div>')
                    st.checkbox(L["qr_check"], key="qr_on")
            else:
                st.info(L["share_addr"])
            st.caption(L["share_note"])
        md(cv_html(d, st.session_state.tpl, TH, photo, qr=_qr))
        md(ad_slot())

# =====================================================================
# القوالب
# =====================================================================
elif page == "templates":
    md(f'<div class="ptitle">{html.escape(L["t_title"])}</div><div class="psub">{html.escape(L["t_sub"])}</div>')
    cols = st.columns(3, gap="medium")
    for col, tp in zip(cols, TPLS):
        with col:
            md(f'<div class="thumb">{cv_html(demo, tp, TH)}</div>'
               f'<div class="tname">{html.escape(L["tpl_names"][tp])}</div>'
               f'<div class="tdesc">{html.escape(L["tpl_desc"][tp])}</div>')
            if st.session_state.tpl == tp:
                st.caption("✅ " + L["t_cur"])
            st.button(L["t_use"], on_click=go, args=("builder", tp), key=f"use_{tp}", use_container_width=True, type="primary")
    md(ad_slot())

# =====================================================================
# كيف يعمل + الأسئلة الشائعة + الخصوصية والشروط
# =====================================================================
elif page == "how":
    md(f'<div class="ptitle">{html.escape(L["how_title"])}</div>')
    steps = "".join(f'<div class="fc stp"><div class="n">{n}</div><div><h5 style="margin-top:0">{html.escape(t)}</h5><p>{html.escape(x)}</p></div></div>'
                    for n, (t, x) in enumerate(L["steps"], 1))
    md(f'<div class="grid3" style="margin-bottom:10px">{steps}</div>')
    md(f'<div class="h2s">{html.escape(L["faq_title"])}</div>')
    for q, a in L["faqs"]:
        with st.expander(q):
            st.write(a)
    with st.expander("🔒 " + L["priv_title"]):
        st.write(L["priv_text"])
    with st.expander("📄 " + L["terms_title"]):
        st.write(L["terms_text"])
    md(resources_html())

# =====================================================================
# تواصل معنا
# =====================================================================
elif page == "contact":
    md(f'<div class="ptitle">{html.escape(L["c_title"])}</div><div class="psub">{html.escape(L["c_sub"])}</div>')
    e = html.escape
    cards = []
    if CONTACT["email"]:
        cards.append(f'<div class="fc"><div class="ic">✉️</div><h5>{e(L["c_email"])}</h5><a href="mailto:{e(CONTACT["email"], quote=True)}">{e(CONTACT["email"])}</a></div>')
    if CONTACT["phone"]:
        cards.append(f'<div class="fc"><div class="ic">📱</div><h5>{e(L["c_phone"])}</h5><a href="tel:{e(CONTACT["phone"].replace(" ", ""), quote=True)}" dir="ltr">{e(CONTACT["phone"])}</a></div>')
    if CONTACT["loc"][lang]:
        cards.append(f'<div class="fc"><div class="ic">📍</div><h5>{e(L["c_loc"])}</h5><p>{e(CONTACT["loc"][lang])}</p></div>')
    socials = " &nbsp;•&nbsp; ".join(
        f'<a href="{e(u, quote=True)}" target="_blank" rel="noopener">{n}</a>'
        for n, u in (("LinkedIn", CONTACT["linkedin"]), ("GitHub", CONTACT["github"]), ("X", CONTACT["x"])) if u)
    if socials:
        cards.append(f'<div class="fc"><div class="ic">🌐</div><h5>{e(L["c_social"])}</h5><p>{socials}</p></div>')
    if cards:
        md(f'<div class="grid3">{"".join(cards)}</div>')
    else:
        st.info(L["c_empty"])
    if CONTACT["email"]:
        md(f'<div class="h2s">{e(L["c_form"])}</div>')
        _, mid, _ = st.columns([1, 3, 1])
        with mid:
            cn = st.text_input(L["c_name"], key="cf_name")
            cm = st.text_input(L["c_mail"], key="cf_mail")
            cg = st.text_area(L["c_msg"], key="cf_msg", height=140)
            body = f"{cg}\n\n{cn}\n{cm}"
            st.link_button(L["c_send"], f"mailto:{CONTACT['email']}?subject={quote(L['c_subject'])}&body={quote(body)}",
                           use_container_width=True, disabled=not cg.strip(), type="primary")
            st.caption(L["c_hint"])

elif page in ("about", "privacy", "terms"):
    _key = {"about": "about", "privacy": "privp", "terms": "termsp"}[page]
    md(f'<div class="ptitle">{html.escape(L[_key + "_title"])}</div><div class="psub">{html.escape(L["pg_updated"])}</div>')
    for _h, _t in L[_key + "_secs"]:
        if "{email}" in _t:
            if not CONTACT["email"]:
                continue
            _t = _t.replace("{email}", CONTACT["email"])
        md(f'<div class="fc" style="margin-bottom:12px"><h5>{html.escape(_h)}</h5><p>{html.escape(_t)}</p></div>')

# =====================================================================
# الفوتر
# =====================================================================
AD_HTML = (f'<br><a class="spons" href="{html.escape(AD_LINK, quote=True)}" target="_blank" rel="noopener sponsored nofollow">📢 {html.escape(L["ad_text"])}</a>' if AD_LINK else "")
_, _f1, _f2, _f3, _ = st.columns([2, 1.2, 1.2, 1.2, 2])
_f1.button(L["f_priv"], on_click=go, args=("privacy",), key="ft_priv", use_container_width=True)
_f2.button(L["f_terms"], on_click=go, args=("terms",), key="ft_terms", use_container_width=True)
_f3.button(L["f_about"], on_click=go, args=("about",), key="ft_about", use_container_width=True)
md(f'<div class="foot"><b>✨ Lumina CV</b><br>© 2026 &nbsp;|&nbsp; {html.escape(L["footer"])}<br>{html.escape(L["footer2"])}{AD_HTML}</div>')
