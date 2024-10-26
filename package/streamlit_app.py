import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
import seaborn as sns
from bidi.algorithm import get_display  # Fixes Arabic display
import arabic_reshaper  # Reshapes Arabic characters for display
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from package import Jadarat_Jobs as jb

# Title and Introduction
st.title("مقدمة: فهم سوق العمل السعودي للخريجين الجدد (جدرات)" )
st.markdown(
    """
  تخيل أنك في بداية رحلتك المهنية, خرجت للتو من الجامعة وتتطلع لمعرفة سوق العمل السعودي. قد تخطر في عقلك مجموعة من الأسئلة, هل هناك فرصة كبيرة لشخص معدوم الخبرة؟ ما هو نطاق متوسط الرواتب؟ أي نوع من الشركات توظف الخريجين الجدد؟
  .سنستعرض ثلاث نقاط رئيسية ستمنحك فهمًا قويًا للمشهد الوظيفي الحالي للخريجين الجدد. ينبغي العلم ان جميع المعلومات المذكورة هنا هي بناء على المنصة الوطنية الموحدة للتوظيف (جدارات) التي تربط بين الباحثين عن العمل والفرص المتاحة في القطاعين العام والخاص
    """
    
)


# Section 1: Number of Jobs Based on Experience Level
st.header("1. عدد الوظائف بناءً على الخبرة")
st.markdown(
    """
    غالبًا ما يقلق الخريجون الجدد من أن نقص الخبرة قد يكون عائقًا في الحصول على وظيفة. ولكن الخبر السار هو أن العديد من الجهات تبحث بنشاط عن المواهب الجديدة وتقدّر الحماس والقدرة على التكيف والإمكانيات التي يجلبها الخريجون الجدد. إليك رسمة توضيحية:
    """
    
)

###CHART
st.bar_chart(data=jb.job_opportunities_df, x="Experience", y="Number of posts", x_label="سنوات الخبرة", y_label="عدد الوظائف", width=None, height=None)

st.markdown("هذا يوضح أنه حتى إذا كنت بدون خبرة كبيرة، فهناك الكثير من الوظائف المتاحة خصيصًا للخريجين الذين لديهم استعداد للتعلم.")


# Section 2: Expected Salary Range for Fresh Graduates Based on Job Title
st.header("2. نطاق الراتب المتوقع للخريجين الجدد")
st.markdown("""
بمجرد أن تحصل على وظيفة في المستوى المبتدئ، يأتي السؤال الكبير التالي حول الراتب. تتفاوت رواتب الخريجين الجدد بناءً على الوظيفة، والمهارات المطلوبة، والصناعة. إليك نظرة عامة على متوسط رواتب  بين الخريجين الجدد:
"""
)

###CHART
# What is the expected salary range for fresh graduates? 
# plot range of salary using bar chart
plt.figure(figsize=(10, 5))

#histogram
sns.histplot(jb.avg_salary_fresh_grad_df['salary'], kde=True)

# Apply Arabic reshaping and BiDi to labels to visiualize it correctly in seaborn
xlbl = get_display( arabic_reshaper.reshape('الراتب'))
ylbl = get_display( arabic_reshaper.reshape('عدد الوظائف بهذا الراتب'))

plt.xlabel(xlbl)
plt.ylabel(ylbl)

# Apply Arabic reshaping and BiDi to title to visiualize it correctly in seaborn
title = get_display(arabic_reshaper.reshape('النطاق المتوقع للراتب لحديثي التخرج') )
plt.title(title)

# add plot to streamlit
st.pyplot(plt)

st.markdown(
"""
تختلف نطاقات الرواتب حسب الوظيفة, نوع الشركة, المهارات المطلوبة. رغم ان هذه تقديرات تقريبية فإن فهم نطاق متوسط الرواتب يساعد في فهم سوق العمل للخريجين الجدد.
"""
)

# Section 3: Company Types Hiring Fresh Graduates

st.header("3. أنواع الشركات التي توظف الخريجين الجدد بشكل مكثف")
st.markdown("""
        الآن بعد أن أصبح لديك شعور بتوافر الوظائف وتوقعات الراتب ، فإن الخطوة التالية هي تحديد أنواع الشركات التي من المرجح أن توظفك. تقوم بعض القطاعات بتوظيف الخريجين الجدد بنشاط ، مع إدراك إمكاناتهم للنمو والأفكار الجديدة. إن معرفة مكان تركيز البحث يمكن أن يوفر لك الوقت ويزيد من فرصك في الحصول على وظيفة.
            """
             )
###CHART
st.bar_chart(data=jb.no_exp_comp_type_df, x="نوع الشركة", y="عدد الوظائف")

st.markdown(
    """
    يوضح هذا الرسم البياني أن الشركات الخاصة تنشر غالبية الوظائف التي لا تتطلب خبرة ، في حين  شبه الحكومية أقل. وهذا يشير إلى أن الشركات الخاصة تميل إلى تقديم المزيد من الوظائف المبتدئة، مما يجعلها هدفا قويا للخريجين الجدد الذين يتطلعون إلى بدء حياتهم المهنية.
    """
    
)