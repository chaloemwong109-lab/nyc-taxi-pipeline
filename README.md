# NYC Taxi Data Lifecycle & Pipeline (Submission 2)

1. Project Overview & Research Question
Pipeline นี้พัฒนาขึ้นเพื่อประมวลผลข้อมูล NYC Taxi ในช่วงครึ่งปีแรกของปี 2024 (มกราคม - มิถุนายน) เพื่อตอบคำถาม:
> **"Which taxi type was the most used in the first half of 2024?"**

**เกณฑ์การวัด (Metric Definition):** 
คำว่า "most used" วัดจาก **จำนวนเที่ยวการเดินทางที่ถูกต้องตามเกณฑ์ (Total Valid Trip Records)** และคำนวณสัดส่วนส่วนแบ่งตลาด (Market Share %)



2. Pipeline Architecture & Data Flow Diagram





รายละเอียดแต่ละ Layer:
Ingestion Layer (src/ingest.py): สตรีมดาวน์โหลด Parquet รายเดือน พร้อมระบบ Retry 3 ครั้ง และตรวจสอบ Cache ในเครื่องเพื่อลดภาระแบนด์วิดท์

Transformation Layer (src/transform.py): ทำ Schema Harmonization แปลงชื่อคอลัมน์ให้อยู่ในมาตรฐานเดียวกัน กรอง Outlier วันที่ข้ามปี และกรองระยะทางติดลบ

Data Quality Gate (src/quality.py): ตรวจสอบความถูกต้องของข้อมูล (Missing, Timestamp Bound, Distance Validations) ก่อนอนุญาตให้บันทึกลง Curated Layer

Curated Storage (data/curated/): จัดเก็บไฟล์ Parquet สะอาด พร้อมแยกไฟล์ sample_*.parquet ขนาด 1,000 แถวสำหรับเป็นตัวอย่างพร้อมใช้

Analytics Layer (src/analyze.py): รวมผลลัพธ์คำนวณสัดส่วนการเดินทางและส่งออกตารางสรุป

3. How to Setup and Run
Prerequisites
-Python 3.9+
-Git
# Clone repository
git clone <YOUR-GITHUB-REPO-URL>
cd nyc-taxi-pipeline

# สร้าง Environment และติดตั้ง Dependencies
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

# สั่งรัน Pipeline ทั้งหมด
python main.py

4. Execution Evidence & Status


5. Data Quality Report
ผลการตรวจสอบคุณภาพข้อมูลระหว่างการทำงาน (ดูข้อมูลละเอียดได้ที่ outputs/quality_report.csv):

Timestamp Boundary Check: ตรวจพบและตัดแถวที่บันทึกวันเวลานอกช่วงครึ่งปีแรกของ 2024 (เกิดจากนาฬิกามิเตอร์ผิดพลาดหรือบันทึกข้ามปี) ออกทั้งหมด

Negative Distance Check: กรองข้อมูลระยะทางติดลบออก

Curated Dataset Status: ทุกไฟล์ผ่านเกณฑ์ Quality Gate (PASSED) 100%

6. Key Analytical Findings
ผลลัพธ์จากการประมวลผลครึ่งปีแรกของปี 2024 (H1 2024):
Taxi Type,Total Valid Trips,Market Share (%)
High-Volume FHV (fhvhv),"120,064,668",85.39%
Yellow Taxi (yellow),"20,331,944",14.37%
Green Taxi (green),"339,763",0.24%
Total,"140,736,375",100.00%

คำตอบของโจทย์: ประเภทแท็กซี่ที่มีการใช้งานมากที่สุดในครึ่งปีแรกของปี 2024 คือ High-Volume For-Hire Vehicles (FHVHV - Uber/Lyft) คิดเป็น 85.39% ของการเดินทางทั้งหมด

7. Key Design Decisions
Decision 1: การแบ่งโครงสร้างเป็น Modular Scripts แทนการใช้ Notebook เดียว

เหตุผล: โค้ด Notebook เดิมใน Submission 1 ต้องกดรันทีละ Cell เสี่ยงต่อ Human Error และไม่สามารถสั่งรันอัตโนมัติแบบ End-to-End ได้ การแยกเป็น ingest, transform, quality, analyze ทำให้โค้ดรันซ้ำได้ มีระเบียบ และสามารถขยายต่อยอดได้ง่าย

Decision 2: การเลือกใช้ Parquet Format สำหรับ Curated Output และการสตรีม I/O

เหตุผล: ข้อมูลมีขนาดใหญ่กว่า 140 ล้านแถว การใช้ Parquet ควบคู่กับ Snappy Compression ช่วยประหยัดพื้นที่สตอเรจลงมหาศาล และทำให้โมดูล analyze สามารถเลือกโหลดเฉพาะคอลัมน์ taxi_type มานับจำนวนแถวได้ทันทีโดยไม่ต้องโหลดข้อมูลทั้งหมดเข้า RAM

8. Comparison with Submission 1
Submission 1 (Data Lifecycle Baseline): เป็นการสำรวจข้อมูลเบื้องต้นบน Google Colab เน้นการทำ Exploratory Data Analysis (EDA) และ Data Lifecycle แบบ Manual ขาดระบบ Logging ไม่มีระบบตรวจสอบ Data Quality ระหว่างการทำงาน และต้องดาวน์โหลดข้อมูลซ้ำ

Submission 2 (Reproducible Pipeline): ปรับเป็น Automated Pipeline ที่มี Idempotency (มี Cache ไม่โหลดซ้ำ), มีระบบ Data Quality Gate ป้องกัน Bad Data, มีการจัดเก็บ Curated Data พร้อม Sample ให้ตรวจสอบ และมี Logging บันทึกสถานะการทำงานทุกขั้นตอนอย่างชัดเจน

9. Limitations
การประมวลผลยังใช้ Pandas เป็นหลัก ซึ่งใช้หน่วยความจำ RAM ของเครื่อง (In-memory) หากข้อมูลขยายเป็นระดับหลายปี อาจต้องขยายระบบไปใช้ Distributed Framework เช่น Apache Spark หรือเครื่องมืออย่าง DuckDB/Polars

บริการ FHVHV ไม่มีการบันทึกคอลัมน์จำนวนผู้โดยสาร (passenger_count) ทำให้ไม่สามารถเปรียบเทียบในมิติของจำนวนผู้โดยสารรวมได้ จึงต้องใช้จำนวนเที่ยวการเดินทาง (Valid Trips) เป็นตัวชี้วัดหลัก

10. Learning Reflection
การทำ Submission 2 ทำให้เข้าใจหัวใจสำคัญของ Data Engineering ว่าไม่ได้อยู่ที่การเขียนโค้ดเพื่อให้ได้ผลลัพธ์เพียงครั้งเดียว แต่อยู่ที่การออกแบบ Pipeline ที่มีความเป็นระบบ รันซ้ำได้ (Reproducible) และตรวจสอบที่มาของผลลัพธ์ย้อนกลับได้ การสร้าง Data Quality Gate และ Logging ช่วยให้มั่นใจในความถูกต้องของข้อมูลก่อนนำไปส่งต่อให้ชั้นวิเคราะห์ ซึ่งช่วยลดความผิดพลาดในการตัดสินใจทางธุรกิจได้อย่างมาก