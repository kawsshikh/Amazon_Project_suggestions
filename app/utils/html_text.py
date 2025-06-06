import pandas as pd
from app.services.table_format import *
get_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Product Finder</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #f97316; /* soft orange */
      font-family: "Segoe UI", Tahoma, sans-serif;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .form-container {
      backdrop-filter: blur(15px);
      background-color: rgba(255, 255, 255, 0.65);
      border-radius: 30px;
      padding: 50px 35px;
      width: 90%;
      max-width: 600px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      text-align: center;
    }

    h2 {
      color: #15803d; /* green-700 */
      font-size: 1.9em;
      margin-bottom: 10px;
    }

    p {
      font-size: 1em;
      color: #333;
      margin-bottom: 20px;
      line-height: 1.5;
    }

    input[type="text"] {
      width: 90%;
      max-width: 420px;
      padding: 14px 20px;
      border: 1px solid #ccc;
      border-radius: 12px;
      font-size: 1em;
      margin-bottom: 20px;
      outline: none;
      transition: border-color 0.3s ease;
      background-color: rgba(255, 255, 255, 0.85);
    }

    input[type="text"]:focus {
      border-color: #16a34a;
    }

    button {
      background-color: #22c55e;
      color: white;
      padding: 12px 30px;
      border: none;
      border-radius: 10px;
      font-size: 1em;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #15803d;
    }

    .footer-note {
      font-size: 0.85em;
      color: #111;
      margin-top: 20px;
    }
  </style>
</head>
<body>

  <div class="form-container">
    <h2>✨ What do you wanna find today?</h2>
    <p class="subtitle">Try something like:<br><em>“Top 5 noise-canceling headphones with 3.5+ rating, not sponsored”</em></p>

    <form action="/result" method="post">
      <input type="text" name="question" placeholder="What's on your mind?" required />
      <br />
      <button type="submit">Let’s Go 🚀</button>
    </form>

    <div class="footer-note">
      I can filter by ⭐ rating, 🏷️ ads, and how many results.<br>
      <em>(Price filter coming soon!)</em>
    </div>
  </div>

</body>
</html>
"""
def gen_html(df, json_query):
    html_start  = """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Earphone Finder</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #f97316; /* soft orange */
      font-family: "Segoe UI", Tahoma, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .form-container {
      backdrop-filter: blur(15px);
      background-color: rgba(255, 255, 255, 0.65);
      border-radius: 30px;
      padding: 50px 35px;
      width: 90%;
      max-width: 600px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      text-align: center;
      margin-top: 60px;
    }

    h2 {
      color: #1e3a8a; /* blue tone for better blend */
      font-size: 1.9em;
      margin-bottom: 10px;
    }

    .suggestion-heading {
      color: #1e3a8a;
      font-size: 1.4em;
      margin: 40px auto 10px;
      text-align: center;
    }

    p {
      font-size: 1em;
      color: #333;
      margin-bottom: 20px;
      line-height: 1.5;
    }

    input[type="text"] {
      width: 90%;
      max-width: 420px;
      padding: 14px 20px;
      border: 1px solid #ccc;
      border-radius: 12px;
      font-size: 1em;
      margin-bottom: 20px;
      outline: none;
      transition: border-color 0.3s ease;
      background-color: rgba(255, 255, 255, 0.85);
    }

    input[type="text"]:focus {
      border-color: #1e40af;
    }

    button {
      background-color: #1d4ed8;
      color: white;
      padding: 12px 30px;
      border: none;
      border-radius: 10px;
      font-size: 1em;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #1e40af;
    }

    .footer-note {
      font-size: 0.85em;
      color: #111;
      margin-top: 20px;
    }

    /* 🎯 Product Ribbons Section */
    .ribbon-wrapper {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin: 40px auto 60px;
      width: 100%;
    }

    .product-ribbon {
      display: flex;
      align-items: center;
      background-color: rgba(255, 255, 255, 0.85);
      border-radius: 20px;
      padding: 12px 18px;
      margin: 12px 0;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      width: 90%;
      max-width: 600px;
      transition: transform 0.2s ease;
      animation: popIn 0.3s ease;
    }

    .product-ribbon:hover {
      transform: scale(1.02);
    }

    .product-ribbon img {
      width: 80px;
      height: 80px;
      object-fit: cover;
      border-radius: 12px;
      margin-right: 20px;
    }

    .product-info {
      flex: 1;
      display: flex;
      flex-direction: column;
    }

    .product-title {
      font-size: 1.1em;
      font-weight: bold;
      color: #1e3a8a;
      text-decoration: none;
      margin-bottom: 6px;
    }

    .product-title:hover {
      text-decoration: underline;
    }

    .product-meta {
      font-size: 0.95em;
      color: #111;
    }

    @keyframes popIn {
      from {
        transform: translateY(20px);
        opacity: 0;
      }
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }
  </style>
</head>
<body>"""

    df_len = len(df)
    json_len = json_query["limit"]
    max_sugg = min(json_len, json_len)
    final_df = df.head(max_sugg)
    spn = "Sponsored" if json_query["sponsored"] else "Not Sponsored"
    start = f'''<h2 class="suggestion-heading">🎧 {max_sugg} Suggestions for {json_query["query"]} with {json_query["stars"]}+ Star Rating and {spn}</h2>'''

    for index, row in final_df.iterrows():
        name = row['SkuName']
        image_url = row['ImageUrl']
        skuUrl = row['SkuUrl']
        price = row["SalePrice"]
        reviews = row['Reviews']
        pms = int(row['PastMonthsales']) if row['PastMonthsales'] else None
        sponsored = "sponsored" if row['sponsored'] else "Not Sponsored"
        rating = row['Rating']
        ribbon = f"""
        <div class="product-ribbon">
        <img src={image_url} alt={name} />
        <div class="product-info">
        <a href="{skuUrl}" class="product-title">{name}</a>
        <div class="product-meta">{price} | ⭐ {rating} | {reviews} reviews | 🏷️ {sponsored} | {pms} sold last month </div>
        </div>
        </div>"""
        start += ribbon

    return (html_start+start + "</body></html>")


