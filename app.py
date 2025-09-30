import gradio as gr
import pandas as pd
import subprocess
import sys
import os
from datetime import datetime, timedelta

def simulate_agent_run():
    """
    هذه الدالة تحاكي دورة عمل الوكيل الذكي الكاملة مع تشخيص ديناميكي للحالات.
    """
    # ---- 1. محاكاة السجلات (Logs) ----
    logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] بدء الدورة اليومية المجدولة...",
        f"[{datetime.now().strftime('%H:%M:%S')}] تم الاتصال بقاعدة البيانات... تم سحب 89,280 قراءة جديدة.",
        f"[{datetime.now().strftime('%H:%M:%S')}] تحديد نافذة التدريب: من {(datetime.now() - timedelta(days=60)).strftime('%d-%m-%Y')} إلى {datetime.now().strftime('%d-%m-%Y')}.",
    ]
    
    # ---- 2. تشغيل الكود الفعلي للكشف ----
    try:
        process = subprocess.run(
            [sys.executable, 'detector.py'],
            capture_output=True, text=True, encoding='utf-8'
        )
        if process.returncode != 0:
            return "<div style='text-align:center; padding: 20px; font-family: Cairo, sans-serif;'><p style='font-size: 18px; color:red;'>🔴 حدث خطأ أثناء تشغيل الكشف!</p></div>", f"<div style='text-align:center; padding: 20px; color:#95a5a6; font-family: monospace;'>{process.stderr}</div>", "فشل!"

        logs.extend([
            f"[{datetime.now().strftime('%H:%M:%S')}] بدء تدريب النماذج على 30 عميل...",
            f"[{datetime.now().strftime('%H:%M:%S')}] اكتمل التدريب. بدء عملية الكشف...",
            f"[{datetime.now().strftime('%H:%M:%S')}] تم كشف 10 حالات مشتبه بها.",
            f"[{datetime.now().strftime('%H:%M:%S')}] تم إنشاء 10 ملفات قضايا."
        ])

        # ---- 3. إنشاء ملفات القضايا بتصميم وتشخيص ديناميكي ----
        results_df = pd.read_csv('anomaly_results.csv')
        case_files_html = "<div style='direction: rtl;'>"
        # استخدام enumerate للحصول على الترتيب (0, 1, 2, ...)
        for i, (index, row) in enumerate(results_df.head(10).iterrows()):
            customer_id = int(row['Customer_ID'])
            score = row['Anomaly_Score']
            
            # تحديد مستوى الخطورة
            if score < -1000:
                severity = "مرتفع جدًا"
                color = "#e74c3c"
            elif score < -500:
                severity = "مرتفع"
                color = "#e67e22"
            else:
                severity = "متوسط"
                color = "#f1c40f"
            
            # *** هنا التعديل: منطق التشخيص الديناميكي ***
            if i == 0: # الحالة الأولى (الأعلى خطورة)
                diagnosis_html = """
                    <p style='font-weight: 600; color:#2c3e50; margin-top:0;'>تشخيص الذكاء الاصطناعي:</p>
                    <ul style='padding-right: 20px; margin-top: 5px; margin-bottom: 15px;'>
                        <li>تم رصد هبوط ملحوظ في الجهد لا يتناسب مع الاستهلاك المنخفض المسجل.</li>
                        <li>يشير ذلك باحتمالية عالية لوجود حمل غير مقاس (سرقة).</li>
                    </ul>
                    <p style='font-weight: 600; color:#2c3e50;'>الإجراء الموصى به:</p>
                     <ul style='padding-right: 20px; margin-top: 5px; margin-bottom: 0;'>
                        <li><strong>أولوية قصوى:</strong> إرسال فريق التفتيش للتحقق المادي الفوري.</li>
                    </ul>
                """
            else: # باقي الحالات
                diagnosis_html = """
                    <p style='font-weight: 600; color:#2c3e50; margin-top:0;'>تشخيص الذكاء الاصطناعي:</p>
                    <ul style='padding-right: 20px; margin-top: 5px; margin-bottom: 15px;'>
                        <li>تم رصد تناقض طفيف بين قراءات الجهد والاستهلاك.</li>
                    </ul>
                    <p style='font-weight: 600; color:#2c3e50;'>الإجراء الموصى به:</p>
                     <ul style='padding-right: 20px; margin-top: 5px; margin-bottom: 0;'>
                        <li>إضافة العميل لقائمة المراقبة والتحقق الدوري.</li>
                    </ul>
                """

            case_files_html += f"""
            <div style='border: 1px solid #ecf0f1; border-right: 7px solid {color}; padding: 20px; margin-bottom: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 4px 8px rgba(0,0,0,0.05); font-family: Cairo, sans-serif;'>
                <h3 style='color: #34495e; margin-top:0; text-align:center;'>ملف قضية: العميل رقم {customer_id}</h3>
                <hr style='border-top: 1px solid #ecf0f1;'>
                <p style='font-size: 1.2em; font-weight: bold;'>درجة الشبهة: <span style='color: {color};'>{score:.2f}</span> (خطورة: {severity})</p>
                <p style='color:#7f8c8d;'><strong>العنوان (مثال):</strong> {100 + customer_id} شارع المحطة، القاهرة</p>
                <div style='background-color: #f8f9f9; padding:15px; border-radius:8px; margin-top:15px;'>
                    {diagnosis_html}
                </div>
            </div>
            """
        case_files_html += "</div>"

        # ---- 4. محاكاة إرسال البريد الإلكتروني وتحديث الحالة ----
        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] تم إرسال بريد إلكتروني بالتقرير اليومي إلى inspection-lead@power-company.com.")
        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] اكتملت الدورة بنجاح. العودة إلى وضع الخمول.")
        
        agent_status_html = """
        <div style='text-align:center; padding: 20px; font-family: Cairo, sans-serif; direction: rtl;'>
            <p style='font-size: 18px; color:#27ae60;'>🟢 <strong>الحالة:</strong> خامل، في انتظار الدورة المجدولة التالية (2:00 AM غدًا).</p>
        </div>
        """
        
        return agent_status_html, case_files_html, "\n".join(logs)

    except Exception as e:
        return "<div style='text-align:center; padding: 20px; font-family: Cairo, sans-serif;'><p style='font-size: 18px; color:red;'>🔴 حدث خطأ!</p></div>", f"<div style='text-align:center; padding: 20px; color:#95a5a6; font-family: monospace;'>خطأ غير متوقع: {str(e)}</div>", ""

# --- تصميم واجهة Gradio النهائية ---
with gr.Blocks(theme=gr.themes.Soft(), title="نظام حماة الكهرباء (الوكيل الذكي)") as demo:
    demo.head = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        .tab-buttons { justify-content: center !important; }
    </style>
    """
    
    gr.HTML("<div style='text-align:center; font-family: Cairo, sans-serif;'><h1 style='color:#2c3e50;'>💡 نظام حماة الكهرباء (إصدار الوكيل الذكي)</h1><h3 style='color:#34495e;'>للكشف الذكي عن سرقة الطاقة باستخدام الذكاء الاصطناعي</h3></div>")
    gr.Markdown("<hr>")
    
    with gr.Tabs() as tabs:
        # --- القسم الأول: لوحة التحكم ---
        with gr.TabItem("Dashboard | لوحة التحكم", id=0):
            agent_status_text = gr.HTML("<div style='text-align:center; padding: 20px; font-family: Cairo, sans-serif; direction: rtl;'><p style='font-size: 18px; color:#566573;'>⚪ <strong>الحالة:</strong> غير معروف (يرجى تشغيل الدورة).</p></div>")
            run_button = gr.Button("▶️ تشغيل دورة الكشف اليومية يدويًا (محاكاة)", variant="primary", size="lg")

        # --- القسم الثاني: تقرير الحالات ---
        with gr.TabItem("Daily Report | تقرير الحالات اليومي", id=1):
            gr.HTML("<h2 style='text-align:center; font-family: Cairo, sans-serif;'>تقرير الحالات المشتبه بها لليوم</h2>")
            case_files_output = gr.HTML("<div style='text-align:center; padding: 20px; color:#95a5a6; font-family: Cairo, sans-serif;'>لا توجد حالات لعرضها. يرجى تشغيل دورة الكشف أولاً.</div>")

        # --- القسم الثالث: سجلات النظام ---
        with gr.TabItem("System Logs | سجلات النظام", id=2):
            gr.HTML("<h2 style='text-align:center; font-family: Cairo, sans-serif;'>سجلات عمل الوكيل الذكي</h2>")
            logs_output = gr.Code(value="...في انتظار بدء العملية...")
    
    # ربط زر التشغيل بالدالة الرئيسية
    run_button.click(
        fn=simulate_agent_run,
        inputs=[],
        outputs=[agent_status_text, case_files_output, logs_output]
    )

if __name__ == "__main__":
    demo.launch()
