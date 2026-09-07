import streamlit as st
import json
import os

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة أعمال الشركات", page_icon="💼", layout="wide")

# تغيير اتجاه الموقع ليدعم اللغة العربية
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    button { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# اسم ملف قاعدة البيانات الثابتة
DB_FILE = 'companies_db.json'

# دالة لقراءة البيانات من الملف الثابت
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # بياناتك الافتراضية تظهر دائماً في البداية
        return [
            {
                "name": "شركة الإبداع للبرمجيات",
                "title": "تطبيق متجر إلكتروني ذكي",
                "desc": "قمنا بتصميم وبرمجة متجر إلكتروني متكامل يدعم الدفع بالفيزا ومدعوم بالذكاء الاصطناعي لتوقع سلوك المستهلك.",
                "image": "https://unsplash.com",
                "whatsapp": "212707193526",
                "email": "ourachem@gmail.com"
            }
        ]

# دالة لحفظ البيانات في الملف الثابت لكي لا تضيع أبداً
def save_data(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# تحميل البيانات عند فتح الموقع
if 'companies_data' not in st.session_state:
    st.session_state.companies_data = load_data()

# عنوان الموقع الرئيسي
st.title("💼 منصة عرض أعمال الشركات والتعاقدات")
st.write("المكان الأفضل للشركات لاستعراض مشاريعها وللعملاء للوصول المباشر.")
st.markdown("---")

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
                st.session_state.companies_data.append(new_project)
                save_data(st.session_state.companies_data) # حفظ في قاعدة البيانات فوراً
                st.success(f"🎉 تم نشر مشروع شركة ({c_name}) بنجاح في المعرض الدائم!")
                st.rerun()
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
        for index, comp in enumerate(st.session_state.companies_data):
            with st.container():
                st.markdown(f"### **{comp['title']}**")
                st.caption(f"بواسطة: **{comp['name']}**")
                
                try:
                    st.image(comp['image'], use_container_width=True)
                except:
                    st.warning("تعذر تحميل صورة هذا المشروع.")
                
                st.write(comp['desc'])
                
                # إصلاح الرابط بإضافة الشرطة المائلة الصحيحة تلقائياً
                clean_whatsapp = comp['whatsapp'].replace('+', '').replace(' ', '')
                whatsapp_link = f"https://wa.me{clean_whatsapp}"
                email_link = f"mailto:{comp['email']}?subject=طلب تعاقد من منصة الأعمال"
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    st.link_button(f"💬 تواصل عبر الواتساب", whatsapp_link, type="primary", use_container_width=True)
                with btn_col2:
                    st.link_button(f"✉️ راسلهم عبر الإيميل", email_link, use_container_width=True)
                
                st.markdown("---")

# ----------------------------------------------------
# القسم الثالث: لوحة تحكم الإدارة السرية (خاصة بك أنت فقط)
# ----------------------------------------------------
st.markdown("<br><br><br>", unsafe_allow_html=True)
with st.expander("🔒 لوحة تحكم مدير المنصة السريّة"):
    admin_password = st.text_input("أدخل كلمة مرور المدير لرؤية خيارات الحذف:", type="password")
    if admin_password == "1234": # كلمة المرور الخاصة بك
        st.success("مرحباً بك يا مدير المنصة! يمكنك الآن حذف أي مشروع مخالف:")
        for idx, comp in enumerate(st.session_state.companies_data):
            col_admin1, col_admin2 = st.columns([4, 1])
            with col_admin1:
                st.write(f"شركة: {comp['name']} - مشروع: {comp['title']}")
            with col_admin2:
                if st.button(f"❌ حذف", key=f"del_{idx}"):
                    st.session_state.companies_data.pop(idx)
                    save_data(st.session_state.companies_data) # تحديث قاعدة البيانات بعد الحذف
                    st.success("تم الحذف بنجاح!")
                    st.rerun()
