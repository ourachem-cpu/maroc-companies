import streamlit as st

# إعدادات الصفحة الأساسية (تظهر أعلى المتصفح)
st.set_page_config(page_title="منصة أعمال الشركات", page_icon="💼", layout="wide")

# تغيير اتجاه الموقع ليدعم اللغة العربية من اليمين لليسار
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    button { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# إنشاء مخزن مؤقت للبيانات إذا لم يكن موجوداً من قبل
if 'companies_data' not in st.session_state:
    st.session_state.companies_data = [
        # 🟢 تم دمج رقم الواتساب والـ Gmail الخاص بك هنا كبيانات افتراضية للموقع
        {
            "name": "شركة الإبداع للبرمجيات",
            "title": "تطبيق متجر إلكتروني ذكي",
            "desc": "قمنا بتصميم وبرمجة متجر إلكتروني متكامل يدعم الدفع بالفيزا ومدعوم بالذكاء الاصطناعي لتوقع سلوك المستهلك.",
            "image": "https://unsplash.com",
            "whatsapp": "212707193526",  # الرقم الخاص بك المعدل برمجياً بدون الصفر الزائد
            "email": "ourachem@gmail.com"  # البريد الإلكتروني الخاص بك
        }
    ]

# عنوان الموقع الرئيسي
st.title("💼 منصة عرض أعمال الشركات والتعاقدات")
st.write("المكان الأفضل للشركات لاستعراض مشاريعها وللعملاء للوصول المباشر.")
st.markdown("---")

# تقسيم الشاشة إلى قسمين: قسم لإدخل البيانات وقسم لعرضها
col1, col2 = st.columns(2)

# ----------------------------------------------------
# القسم الأول: لوحة تحكم الشركات (إضافة عمل جديد)
# ----------------------------------------------------
with col1:
    st.header("➕ أضف عمل شركتك")
    
    with st.form(key='add_company_form', clear_on_submit=True):
        c_name = st.text_input("اسم الشركة *")
        p_title = st.text_input("عنوان المشروع / العمل *")
        p_desc = st.text_area("وصف مختصر للمشروع والأدوات المستخدمة *")
        p_image = st.text_input("رابط صورة للمشروع (رابط URL مباشر) *", value="https://unsplash.com")
        c_whatsapp = st.text_input("رقم الواتساب (مع رمز الدولة وبدون أصفار أو علامة +، مثل: 212707193526) *")
        c_email = st.text_input("البريد الإلكتروني الرسمي (Gmail) *")
        
        submit_button = st.form_submit_button(label="🚀 نشر العمل على المنصة")
        
        if submit_button:
            if c_name and p_title and p_desc and c_whatsapp and c_email:
                new_project = {
                    "name": c_name,
                    "title": p_title,
                    "desc": p_desc,
                    "image": p_image,
                    "whatsapp": c_whatsapp,
                    "email": c_email
                }
                # إضافة المشروع الجديد للمخزن
                st.session_state.companies_data.append(new_project)
                st.success(f"🎉 تم نشر مشروع شركة ({c_name}) بنجاح في المعرض!")
                st.rerun() # إعادة تشغيل الصفحة لتحديث البيانات فوراً
            else:
                st.error("الرجاء ملء جميع الخانات التي تحتوي على علامة (*) ليتم النشر بشكل صحيح.")

# ----------------------------------------------------
# القسم الثاني: معرض الأعمال (ما يراه الزوار والعملاء)
# ----------------------------------------------------
with col2:
    st.header("🖼️ معرض أعمال الشركات الحالية")
    
    if not st.session_state.companies_data:
        st.info("لا توجد أعمال معروضة حالياً، كن أول شركة تضيف عملها!")
    else:
        # عرض كل شركة داخل بطاقة منفصلة
        for index, comp in enumerate(st.session_state.companies_data):
            with st.container():
                st.markdown(f"### **{comp['title']}**")
                st.caption(f"بواسطة: **{comp['name']}**")
                
                # عرض صورة المشروع
                try:
                    st.image(comp['image'], use_container_width=True)
                except:
                    st.warning("تعذر تحميل صورة هذا المشروع (الرابط غير صحيح).")
                
                st.write(comp['desc'])
                
                # روابط وأزرار التواصل الذكية والتفاعلية
                whatsapp_link = f"https://wa.me{comp['whatsapp']}"
                email_link = f"mailto:{comp['email']}?subject=طلب تعاقد من منصة الأعمال"
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.link_button(f"💬 تواصل عبر الواتساب", whatsapp_link, type="primary", use_container_width=True)
                with btn_col2:
                    st.link_button(f"✉️ راسلهم عبر الإيميل", email_link, use_container_width=True)
                
                st.markdown("---")