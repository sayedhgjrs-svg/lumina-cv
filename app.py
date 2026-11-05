import streamlit as st
import os
from PIL import Image

# 1. إعدادات الصفحة والواجهة الاحترافية العريضة
st.set_page_config(page_title="LUMINA CV PRO | مصمم السير الذاتية العالمي", layout="wide", initial_sidebar_state="expanded")

# حقن ستايل CSS سينمائي مبهر مع إخفاء كامل لشعارات وقوائم المنصة لحماية احترافية الموقع
st.markdown("""
    <style>
    /* 🔒 كود سحري لإخفاء شعار وقوائم وأزرار المنصة تماماً من الهاتف والكمبيوتر */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__171of, [data-testid="stViewerBadge"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* تغيير خلفية الموقع بالكامل إلى الوضع الداكن الفاخر */
    .stApp {
        background: linear-gradient(135deg, #0b0914 0%, #110d26 50%, #050409 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* تصميم ورقة المعاينة التفاعلية لتكون بيضاء وأنيقة وتطفو بتأثير ثلاثي الأبعاد */
    .cv-preview-card {
        background-color: #ffffff !important;
        color: #1e293b !important;
        padding: 45px !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 30px rgba(0, 198, 255, 0.1) !important;
        font-family: 'Segoe UI', Arial, sans-serif;
        line-height: 1.6;
        margin-top: 10px;
    }
    
    /* تأثيرات التوهج على حقول المدخلات */
    .stTextInput input, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #00ffcc !important;
        border: 1px solid rgba(255, 0, 127, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease-in-out;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #00ffcc !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.4) !important;
    }
    
    /* تصميم زر الطباعة المتوهج الكبير في الأسفل */
    .print-btn-container .stButton>button {
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 100%) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 22px !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.5) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100%;
        cursor: pointer;
    }
    .print-btn-container .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 40px #00ffcc !important;
        color: #00ffcc !important;
    }
    
    /* ستايلات ورموز التحكم في شكل ورقة السيرة الذاتية أثناء الطباعة الفعلية */
    @media print {
        header, footer, .stSidebar, .stButton, .stFileUploader, .print-btn-container, div[data-testid="stSidebar"] {
            display: none !important;
        }
        .stApp {
            background: white !important;
            color: black !important;
        }
        .cv-preview-card {
            box-shadow: none !important;
            padding: 0 !important;
            margin: 0 !important;
            width: 100% !important;
            border: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية الأنيقة للتحكم بالكامل وفصل اللغتين
st.sidebar.markdown("<h2 style='color:#00ffcc; text-shadow:0 0 10px #00ffcc;'>🌐 الإعدادات / Settings</h2>", unsafe_allow_html=True)
lang = st.sidebar.radio("اختر لغة واجهة الـ CV المستهدفة:", ["العربية", "English"])

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='color:#ff007f;'>📝 بياناتك الشخصية</h3>", unsafe_allow_html=True)

if lang == "العربية":
    align_dir = "right"
    flex_dir = "row-reverse"
    title_main = "✨ لُومِـينَا سْـتُودْيُو لِلسِّيرَة الذَّاتِيَّة الاحتِرَافِيَّة"
    desc_main = "⚡ المنصة العالمية لإنتاج وتصميم السير الذاتية التفاعلية مجاناً. أدخل بياناتك باليسار واطبع ملفك فوراً بضغطة زر!"
    lbl_name, def_name = "الاسم الكامل المربع:", "أحمد محمود العراقي"
    lbl_job, def_job = "المسمى الوظيفي المستهدف:", "مهندس برمجيات ومطور تطبيقات ويب"
    lbl_email, def_email = "البريد الإلكتروني:", "ahmed.developer@email.com"
    lbl_phone, def_phone = "رقم الهاتف والاتصال:", "+20 100 123 4567"
    lbl_summary, def_summary = "النبذة الشخصية (الملخص المهني):", "مطور ويب متكامل وشغوف بخبرة ممتدة في بناء وتطوير الأنظمة الذكية وتطبيقات السيرفر باستخدام لغات البرمجة الحديثة وبايثون."
    lbl_exp, def_exp = "الخبرات العملية السابقة (اكتب كل وظيفة في سطر):", "• مهندس برمجيات رئيسي - شركة التقنية الدولية (2022 - الآن)\n• مطور واجهات خلفية - شركة الحلول الرقمية (2020 - 2022)"
    lbl_edu, def_edu = "المؤهلات التعليمية والشهادات:", "بكالوريوس هندسة الحاسبات والمعلومات - جامعة القاهرة (تقدير ممتاز - 2019)"
    lbl_skills, def_skills = "المهارات التنافسية الأساسية (افصل بينها بفاصلة):", "Python, Streamlit, JavaScript, Docker, SQL, REST APIs, Git"
    btn_print_text = "🚀 اِطبع السيرة الذاتية الآن أو احفظ كـ PDF"
else:
    align_dir = "left"
    flex_dir = "row"
    title_main = "✨ LUMINA PRO INTERACTIVE CV MATRIX"
    desc_main = "⚡ The ultimate world-class engine to build highly attractive professional resumes. Fill your data on the left and print instantly!"
    lbl_name, def_name = "Full Name:", "Alexander Wright"
    lbl_job, def_job = "Target Job Title:", "Senior Full-Stack Web Engineer"
    lbl_email, def_email = "Email Address:", "alex.wright.dev@email.com"
    lbl_phone, def_phone = "Phone Number:", "+1 (555) 019-2834"
    lbl_summary, def_summary = "Professional Summary:", "Results-driven Full Stack Engineer with extensive experience in designing, building, and deploying robust cloud applications and automated enterprise pipelines."
    lbl_exp, def_exp = "Work Experience (One job entry per line):", "• Senior Full-Stack Engineer - NexaTech Solutions (2022 - Present)\n• Software Developer - Quantum Code Systems (2020 - 2022)"
    lbl_edu, def_edu = "Education & Certifications:", "B.Sc. in Computer Engineering - MIT University (GPA 3.9 / 2019)"
    lbl_skills, def_skills = "Core Competitive Skills (Separate with commas):", "Python, Streamlit, Go, React, AWS, Docker, PostgreSQL, CI/CD"
    btn_print_text = "🚀 Launch Print Matrix or Save as PDF"

name = st.sidebar.text_input(lbl_name, def_name)
job_title = st.sidebar.text_input(lbl_job, def_job)
email = st.sidebar.text_input(lbl_email, def_email)
phone = st.sidebar.text_input(lbl_phone, def_phone)
summary = st.sidebar.text_area(lbl_summary, def_summary, height=100)
experience = st.sidebar.text_area(lbl_exp, def_exp, height=120)
education = st.sidebar.text_area(lbl_edu, def_edu, height=80)
skills = st.sidebar.text_input(lbl_skills, def_skills)

uploaded_img = st.sidebar.file_uploader("📸 ارفع صورتك الشخصية من الاستوديو:", type=["jpg", "png", "jpeg"])

st.markdown(f"<h1 style='text-align:center;'>{title_main}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#aaa; font-size:16px; margin-bottom:25px;'>{desc_main}</p>", unsafe_allow_html=True)
st.markdown("---")

st.markdown('<div class="cv-preview-card">', unsafe_allow_html=True)

st.markdown(f"""
    <div style='display: flex; flex-direction: {flex_dir}; justify-content: space-between; align-items: center; width: 100%;'>
        <div style='text-align: {align_dir}; flex-grow: 1;'>
            <h1 style='color: #0f172a !important; margin: 0; font-size: 36px; font-weight: 800;'>{name}</h1>
            <p style='color: #007bff !important; font-size: 22px; font-weight: bold; margin-top: 6px; margin-bottom: 12px;'>{job_title}</p>
            <p style='color: #475569; font-size: 15px; font-weight: 500; margin: 0;'>📧 {email} &nbsp;|&nbsp; 📱 {phone}</p>
        </div>
        <div style='margin-left: 20px; margin-right: 20px;'>
""", unsafe_allow_html=True)

if uploaded_img:
    st.image(Image.open(uploaded_img), width=130)
else:
    st.markdown("<div style='width:120px; height:120px; border-radius:50%; background:#e2e8f0; display:flex; align-items:center; justify-content:center; color:#94a3b8; font-weight:bold; font-size:12px;'>No Photo</div>", unsafe_allow_html=True)

st.markdown("""
        </div>
    </div>
    <hr style='border-top: 3px solid #007bff; margin-top: 25px; margin-bottom: 25px;'>
""", unsafe_allow_html=True)

st.markdown(f"<div style='text-align: {align_dir}; color: #334155;'>", unsafe_allow_html=True)

st.markdown(f"<h3 style='color:#0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;'>🎯 {'الخلاصة المهنية' if lang == 'العربية' else 'Professional Summary'}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:16px; color:#334155;'>{summary}</p>", unsafe_allow_html=True)

st.markdown(f"<h3 style='color:#0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-top: 25px;'>💼 {'الخبرات العملية' if lang == 'العربية' else 'Work Experience'}</h3>", unsafe_allow_html=True)
for exp in experience.split('\n'):
    if exp.strip():
        st.markdown(f"<p style='font-size:15px; margin-bottom: 6px;'>{exp}</p>", unsafe_allow_html=True)

st.markdown(f"<h3 style='color:#0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-top: 25px;'>🎓 {'التعليم والشهادات' if lang == 'العربية' else 'Education & Certifications'}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:15px;'>{education}</p>", unsafe_allow_html=True)

st.markdown(f"<h3 style='color:#0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; margin-top: 25px;'>🛠️ {'المهارات والقدرات الأساسية' if lang == 'العربية' else 'Core Expertise & Skills'}</h3>", unsafe_allow_html=True)
skill_tags = "".join([f"<span style='background:#f1f5f9; color:#1e293b; padding:6px 14px; margin:5px; border-radius:6px; display:inline-block; font-weight:600; font-size:14px; border: 1px solid #cbd5e1;'>{s.strip()}</span>" for s in skills.split(',') if s.strip()])
