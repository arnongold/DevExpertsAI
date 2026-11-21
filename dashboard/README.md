# דשבורד סקרי שירות לקוחות

עותק של הדשבורד שמוצג ב-https://claude.ai/artifact/3oBthQcCU28YoMGbRfjk82

- `index.html`: קוד הדף (גרפים ב-d3 וחישובי המדדים ב-`dash.calc`). הוא רץ בתוך סוג ה-Artifact "Data", שמספק את `dash` ואת `d3`, ולכן לא נפתח כקובץ עצמאי בדפדפן.
- `dashboard-config.json`: הגדרות מקור הנתונים וכותרת הדשבורד, כפי שהם שמורים בדשבורד.

מקור הנתונים הוא `data/survey_analysis.json`, שנוצר מ-`data/customer_service_surveys.csv` בעזרת `data/analyze_surveys.py`.

לעדכון הנתונים:

```bash
python3 data/generate_surveys.py
python3 data/analyze_surveys.py
```

אחר כך צריך להעלות את `survey_analysis.json` החדש לדשבורד, דרך Sources או בבקשה מ-Claude.

העותק כאן לא מתעדכן לבד: שינוי בדשבורד עצמו צריך להעתיק חזרה לריפו.
