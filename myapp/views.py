from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from .models import Stock
from .models import ETF_list
from django.core.cache import cache
from datetime import datetime, timedelta
import twstock
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import io
import base64
import requests
import time
import threading
from django.template.loader import render_to_string


etf_code = [
            '00929','00632R','00665L','00940','00878','00637L','00753L','00919','00650L',
            '00882','00706L','00680L','00939','00941','00934','00752','00715L','00688L',
            '00918','00673R','00900','0056','00945B','00932','00664R','00915','00891',
            '00936','00885','00712','00671R','00927','0050','00881','00655L','00633L',
            '00935','00830','00676R','00923','00713','00642U','00922','00646',
            '00895','00733','00669R','00631L','006208','00700','00690','00892','00902',
            '00893','00930','00907','00757','00692','00731','00662','00905','00645',
            '00909','00921','00896','00675L','00651R','00636','00876','00894',
            '00861','00641R','00640L','00670L','00850','00701','00643','00770','00693U',
            '00897','00901','00904','00638R','00666R','006205','00924','00903','00674R',
            '00926','00728','00635U','0055','00908','00639','00925','00738U','00852L',
            '00681R','00708L','00686R','00763U','00898','0061','00661','00656R',
            '00710B','00911','00652','00678','00654R','00648R','00730','00912','00714',
            '00653L','006207','00683L','00634R','00899','00917','0052',
            '00711B','00865B','00913','00685L','00702','00735','00916','00920',
            '00762','00875','00647L','00910','00657','00703','00709',
            '006206','00736','00783','00717','00737','00739','00668','0051',
            '00682U','00771','00851','0057','00684R','0053','00775B','00660','00663L',
            '006203','00657K','00668K','00689R','006204','00636K','00707R','00625K','00643K'
            ]

etf_name = [
            '復華台灣科技優息','元大台灣50反1','富邦恒生國企正2','元大台灣價值高息','國泰永續高股息',
            '元大滬深300正2','中信中國50正2','群益台灣精選高息','復華香港正2','中信中國高股息',
            '期元大S&P日圓正2','元大美債20正2','統一台灣高息動能','中信上游半導體','中信成長高股息',
            '中信中國50','期街口布蘭特正2','國泰20年美債正2','大華優利高填息30','期元大S&P原油反1',
            '富邦特選高股息30','元大高股息','凱基美國非投等債','兆豐永續高息等權','國泰臺灣加權反1',
            '凱基優選高股息30','中信關鍵半導體','台新永續高息中小','富邦越南','復華富時不動產','富邦NASDAQ反1',
            '群益半導體收益','元大台灣50','國泰台灣5G+','國泰中國A50正2','富邦上証正2','野村臺灣新科技50',
            '國泰費城半導體','富邦臺灣加權反1','群益台ESG低碳50','元大台灣高息低波',
            '期元大S&P石油','國泰台灣領袖50','元大S&P500','富邦未來車','富邦臺灣中小',
            '元大台灣50正2','富邦台50','富邦恒生國企','兆豐藍籌30','富邦台灣半導體','中信電池及儲能',
            '國泰智能電動車','永豐ESG低碳高息','永豐優息存股','統一FANG+','富邦公司治理','復華富時高息低波',
            '富邦NASDAQ','FT臺灣Smart','富邦日本','國泰數位支付服務','兆豐龍頭等權重','中信綠能及電動車',
            '中信上櫃ESG30','復華香港反1','國泰中國A50','元大全球5G','中信小資高價30',
            '元大全球未來通訊','富邦日本反1','富邦日本正2','富邦NASDAQ正2','元大臺灣ESG永續','國泰股利精選30',
            '群益深証中小','國泰北美科技','期街口S&P黃豆','富邦基因免疫生技','永豐智能車供應鏈','新光臺灣半導體30',
            '元大滬深300反1','富邦恒生國企反1','富邦上証','復華S&P500成長','富邦元宇宙','期元大S&P黃金反1',
            '凱基全球菁英55','第一金工業30','期元大S&P黃金','元大MSCI金融','富邦入息REITs+','富邦深100',
            '新光標普電動車','期元大道瓊白銀','國泰美國道瓊正2','元大美債20反1','期元大S&P黃金正2',
            '群益臺灣加權反1','期街口道瓊銅','元大美債7-10','元大寶滬深','元大日經225',
            '國泰中國A50反1','復華彭博非投等債','兆豐洲際半導體','富邦印度','群益那斯達克生技','富邦印度反1',
            '元大S&P500反1','富邦臺灣優質高息','中信臺灣智慧50','群益道瓊美國地產','富邦印度正2',
            '復華滬深','期元大美元指正2','國泰5Y+新興債','FT潔淨能源','元大10年IG電能債',
            '中信特選金融','富邦科技','復華彭博新興債','國泰US短期公債','兆豐台灣晶圓製造',
            '群益臺灣加權正2','國泰標普低波高息','國泰臺韓科技','群益投資級公用債','國泰全球品牌50',
            '國泰A級科技債','國泰A級公用債','國泰網路資安','元大S&P500正2',
            '國泰日經225','國泰A級金融債','台新MSCI中國','富邦歐洲','元大上證50','富邦全球非投等債',
            '富邦中証500','富邦美國特別股','國泰AI+Robo','元大MSCIA股', '國泰美國道瓊', '元大中型100', 
            '元大富櫃50', '期元大美元指數','元大US高息特別股','台新全球AI','富邦摩台', '期元大美元指反1', 
            '元大電子', '新光投等債15+', '元大歐洲50','國泰臺灣加權正2', '元大MSCI台灣', '國泰日經225+U',
            '國泰美國道瓊+U', '國泰20年美債反1','永豐臺灣加權', '國泰中國A50+U', '期元大S&P日圓反1', 
            '富邦上証+R', '群益深証中小+R'
            ]


def stock(request):
    stock_list = Stock.objects.all()  
    return render(request, 'stock.html', {'stock_list': stock_list})

# ETF網頁
def ETF(request):
    for code, name in zip(etf_code, etf_name):
        update_or_create_etf(code, name)

    etf_list = ETF_list.objects.all()
    if request.user.is_authenticated:
        # 將結果返回給網頁
        return render(request, 'ETF_in.html', {'etfs': etf_list})
    else:
        return render(request, 'ETF.html', {'etfs': etf_list})



# 取得ETF資料
db_lock = threading.Lock()
def update_or_create_etf(code, etf_name):
    with db_lock:
        code_with_tw = f"{code}.TW"  # 加上.TW
        try:
            etf_ticker = yf.Ticker(code_with_tw)
            info = etf_ticker.info

            # 檢查是否取得價格資訊
            if 'regularMarketPreviousClose' in info:
                ETF_list.objects.update_or_create(
                    etf_code=code,
                    defaults={
                        'etf_code': code,  
                        'etf_name': etf_name,
                        'price': info.get('regularMarketPreviousClose', 0),
                        'change': info.get('regularMarketChange', 0),
                        'high': info.get('dayHigh', 0),
                        'open': info.get('open', 0),
                        'low': info.get('dayLow', 0),
                        'close': info.get('previousClose', 0),
                        'volume': info.get('regularMarketVolume', 0),
                    }
                )
                # 取得資料後，延遲0.01s
                time.sleep(0.01)
            else:
                print(f"Failed to get market information for ETF code: {code_with_tw}")
        except Exception as e:
            print(f"An error occurred for ETF code: {code_with_tw} - {e}")


# stock新增股票
@require_http_methods("POST")
def stock_add(request):
    # 提取股票代碼
    stock_code = request.POST.get('stock_code').strip() 
    # 檢查代碼是否已在資料庫中
    if Stock.objects.filter(stock_code=stock_code).exists():
        return HttpResponse(f"股票代碼 {stock_code} 已在列表中。", status=400) # status=400 伺服器無法處理這個Request

    if Stock.objects.count() >= 30:
        return HttpResponse("股票列表已滿，無法再新增更多股票。", status=400)

    # stock_info = twstock.realtime.get(stock_code)
    if stock_code:
        try:
            # 獲取股票資訊
            stock_info = twstock.Stock(stock_code)            
            if stock_info.price:
                stock = Stock(                    
                    stock_name=twstock.codes[stock_code].name, 
                    stock_code=stock_code,
                    price=stock_info.price[-1] if stock_info.price else None,
                    change=stock_info.change[-1] if stock_info.change else None,
                    high=stock_info.high[-1] if stock_info.high else None,
                    open=stock_info.open[-1] if stock_info.open else None,
                    low=stock_info.low[-1] if stock_info.low else None,
                    close=stock_info.close[-1] if stock_info.close else None,
                    capacity=stock_info.capacity[-1] if stock_info.capacity else None,
                )
                stock.save()
            else:
                return HttpResponse("非有效股票代碼，請重新確認。", status=400)
        # 獲取股票信息時處理異常
        except Exception as e:  
            return HttpResponse("無法獲取股票資訊。", status=500)    # status=500 伺服器出錯
           
    return redirect("/stock/")

# 刪除stock股票代碼
def stock_delete(request):
    if request.method == 'POST':
        # 從POST請求中取得股票代碼
        stock_code = request.POST['stock_code']
        # 刪除資料庫與股票代碼相同的股票資料
        Stock.objects.filter(stock_code=stock_code).delete()
    return redirect("/stock/")

# 搜尋頁
def stock_search(request):

    # 獲取使用者輸入的代碼，默認為2330
    input_code = request.GET.get('stock_code', '2330').strip()
    # 如果股票代碼不以'TW'結尾且不為'^TWII'，則新增'.TW'
    if not input_code.endswith('.TW') and input_code != '^TWII':
        stock_code = input_code + '.TW'
    else:
        stock_code = input_code

    # 下載台灣的股票數據
    stock = yf.Ticker(stock_code)
    stock_name = stock.info.get('longName',stock_code)
    
    # 取得資料
    df = stock.history(period="3mo")

    # 檢查數據是否成功下載
    if df.empty:
        return HttpResponse("股票數據下載失敗或沒有數據。")
    
    # 使用 mplfinance 庫定制市場顏色和風格。這裡指定上漲為紅色，下跌為綠色。
    color = mpf.make_marketcolors(up='red', down='green', inherit=True)  
    style = mpf.make_mpf_style(base_mpf_style='default', marketcolors=color)

    # K線圖
    # 更改圖的大小
    fig = mpf.figure(style=style, figsize=(10,10))  
    # 新增第一個子圖並新增股票代號標題
    ax1 = fig.add_subplot(2,1,1)
    ax1.set_title(stock_name)  
    # 新增第二個子圖，與第一個子圖共用x軸
    ax2 = fig.add_subplot(2,1,2, sharex=ax1)  
    # 繪製K線圖
    mpf.plot(df, type='candle',mav=(5,10,20), ax=ax1, volume=ax2, xrotation=0)
   
    # 將圖像保存到字節流中，然後將其編碼為 base64 來嵌入HTML中
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    result = '<img src="data:image/png;base64,{}">'.format(figdata_png)
    context = {'chart': result}
    # 會根據用戶是否登入，返回不同的模板和上面定義的 context
    if request.user.is_authenticated:
        return render(request, 'stock_search_in.html', context)
    else:
        return render(request, 'stock_search.html', context)

# 首頁
def index(request):

    # 下載台灣的股票數據
    stock_code = "^TWII"
    stock = yf.Ticker(stock_code)
    
    # 取得資料
    df = stock.history(period="3mo")

    # 檢查數據是否成功下載
    if df.empty:
        return HttpResponse("股票數據下載失敗或沒有數據。")
    
    color = mpf.make_marketcolors(up='red', down='green', inherit=True)  
    style = mpf.make_mpf_style(base_mpf_style='default', marketcolors=color) 

    # K線圖
    # 更改圖的大小
    fig = mpf.figure(style=style, figsize=(8,8))  
    # 新增第一個子圖並新增股票代號標題
    ax1 = fig.add_subplot(2,1,1)
    
   
    # 新增第二個子圖，與第一個子圖共用x軸
    ax2 = fig.add_subplot(2,1,2, sharex=ax1)  
    # 繪製K線圖
    mpf.plot(df, type='candle',mav=(5,10,20), ax=ax1, volume=ax2, xrotation=15)

    # 將圖像保存到字節流中，然後將其編碼為 base64 來嵌入 HTML 中
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    result = '<img src="data:image/png;base64,{}">'.format(figdata_png)
    context = {'tse_chart': result}

    if request.user.is_authenticated:
    # 將結果返回給網頁
        return render(request, 'index_in.html', context)
    else:
        return render(request, 'index.html', context)


def test(request):
    # stock_code = '2330'
    # stock = twstock.Stock(stock_code)
    # bfp = twstock.BestFourPoint(stock)
    # bfp.best_four_point_to_buy()
    # bfp.best_four_point_to_sell()
    # bfp.best_four_point()
    # etf_list = ETF_list.objects.all()
    # stock_code = yf.Ticker('2330.TW')  
    # stock_info = stock_code.info
    # for field in stock_info.keys():
    #     print(field)
    # print(bfp.best_four_point)
    # print(stock)
    # 取得即時資訊
    
    stock = twstock.Stock('2330')
    print(stock)
    return HttpResponse("123")     





############################################
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# user登入後的網頁
@login_required
def index_in(request):
    
    # 下載台灣的股票數據
    stock_code = "^TWII"
    stock = yf.Ticker(stock_code)
    
    # 取得資料
    df = stock.history(period="3mo")

    # 檢查數據是否成功下載
    if df.empty:
        return HttpResponse("股票數據下載失敗或沒有數據。")
    
    color = mpf.make_marketcolors(up='red', down='green', inherit=True)  
    style = mpf.make_mpf_style(base_mpf_style='default', marketcolors=color) 

    # K線圖
    # 更改圖的大小
    fig = mpf.figure(style=style, figsize=(8,8))  
    # 新增第一個子圖並新增股票代號標題
    ax1 = fig.add_subplot(2,1,1)
    
   
    # 新增第二個子圖，與第一個子圖共用x軸
    ax2 = fig.add_subplot(2,1,2, sharex=ax1)  
    # 繪製K線圖
    mpf.plot(df, type='candle',mav=(5,10,20), ax=ax1, volume=ax2, xrotation=15)

    # 將圖像保存到字節流中，然後將其編碼為 base64 來嵌入 HTML 中
    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode()
    result = '<img src="data:image/png;base64,{}">'.format(figdata_png)
    context = {'tse_chart': result}

    # 將結果返回給網頁
    return render(request, 'index_in.html', context)

# 註冊網頁
def register(request):
    return render(request, "register.html")


# 註冊會員
def useradd(request):
    if request.method == "POST":
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        birthday = request.POST["birthday"]
        print(password+" "+repassword+" "+phone+" "+email+" "+birthday)

        #帳號是否重複
        try:
            user = CustomUser.objects.get(email=email) # objects.get 返回符合指定條件的單個對象
        except CustomUser.DoesNotExist:
            user = None

        if user!=None:
            print("帳號已建立")
            message="帳號已建立"
            return render(request,"login.html",locals())
        else:
            if password != repassword:
                message="密碼不一致"
                return render(request,"register.html",locals())
            else:
                #儲存至資料庫
                print("註冊成功")
                user = CustomUser.objects.create_user(email,password)
                user.is_staff = False # 工作人員狀態，設定True則可以登入admin後台
                user.is_active = True
                user.tel = phone
                user.cBirthday = birthday
                user.save()
                return redirect("/index_in/")
    # 如果不是請用POST
    else: 
        return render(request,"/index_in/",locals())
    
# 登入網頁
def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email+" "+password)
        user = authenticate(email=email, password=password) #我改為使用email來驗證
        print(user)
        if user is not None: #驗證通過
            auth.login(request,user) #登入註冊
            return redirect("/index_in/")
            # alert
        else: #驗證未通過
            message="帳號或密碼錯誤"
            return render(request,"login.html",locals())
        # return HttpResponse("已有資料")
    else:
        if 'useradd_success_status' in request.GET: #已註冊成功
            useradd_success_status=True
        return render(request,"login.html",locals())

  

# 登出
def userlogout(request):
    auth.logout(request) #登出
    request.session.flush()  # 清空会话数据
    return redirect("/index/")

#熱門股網頁
def popular(request):
    if request.user.is_authenticated:
        return render(request, "popular_in.html")
    else:
        return render(request, "popular.html")

def monthly(request):
    if request.user.is_authenticated:
        return render(request, "monthly_in.html")
    else:
        return render(request, "monthly.html")

def page1(request):
   return render(request, "page1.html")
    

@csrf_exempt
def api_userlogin(request):
    if request.method == "GET":
        email = request.GET["email"]  # 從 GET 參數中獲取用戶輸入的電子郵件
        password = request.GET["password"]
    elif request.method == "POST":
        email = request.POST["email"]  # 從 POST 參數中獲取用戶輸入的電子郵件
        password = request.POST["password"]
    print(email+" "+password)
    user = authenticate(email=email,password=password) #驗證
    print(user)
    if user is not None: #驗證通過
        return JsonResponse({'result':'true'}, safe=False)
    else: #驗證未通過
        return JsonResponse({'result':'false'}, safe=False)
    








# 待刪除

# @transaction.atomic
# def update_stocks_data():
#     today = datetime.date.today()
#     last_trading_day = today - datetime.timedelta(days=1)
    
#     # 從 twstock 獲取所有股票代碼
#     all_stocks_info = twstock.twse
#     stock_codes = list(all_stocks_info.keys())
    
#     top_stocks = Stock.objects.all().order_by('-capacity')[:30]
#       # Step 3: 更新這些股票資訊至PopularStock模型
#     for stock in top_stocks:
#         PopularStock.objects.update_or_create(
#             stock_code=stock.stock_code,
#             defaults={
#                 'stock_name': stock.stock_name,
#                 'price': stock.price,
#                 'change': stock.change,
#                 'high': stock.high,
#                 'low': stock.low,
#                 'open': stock.open,
#                 'close': stock.close,
#                 'capacity':stock.capacity
#             }
#         )
            
# def popular(request):
#       #先更新全部股票数据
#     update_stocks_data()
    
#     #从数据库取得前一个交易日的所有股票
#     today = datetime.date.today()
#     last_trading_day = today - datetime.timedelta(days=1)
#     stock_list = Stock.objects.filter(date=last_trading_day)
    
#     #取出交易量最大的前30名
#     top30_stocks = stock_list.order_by('-capacity')[:30]
    
#     # print("Stocks: ", stock_list)
#     # print("Top 30 stocks: ", top30_stocks)
#     #返回结果到HTML模板中
#     return render(request, 'popular.html', {'top30_stocks': top30_stocks})

# @transaction.atomic
# def update_all_stocks_data(request):
#     # 從 twstock 獲取所有股票代碼，並遍歷這些代碼
#     all_stocks_info = twstock.twse
#     stock_codes = list(all_stocks_info.keys())

#     for code in stock_codes:
#         # 使用 twstock 獲取具體股票的詳細資料，這需要你實現一個從 code 獲取這些細節的功能
#         stock_info = twstock.Stock(code)
#         latest_info = stock_info.fetch_from(2023, 10)  # 設定你要抓取的時間範圍
#         if latest_info:
#             last_day_info = latest_info[-1]
            
#             PopularStock.objects.update_or_create(
#                 stock_code=code,
#                 defaults={
#                     'stock_name': all_stocks_info[code]['name'],
#                     'price': last_day_info.close,
#                     'change': last_day_info.change,
#                     'high': last_day_info.high,
#                     'open': last_day_info.open,
#                     'low': last_day_info.low,
#                     'close': last_day_info.close,
#                     'capacity': last_day_info.capacity
#                 }
#             )
#     return render(request, 'popular.html', {'top30_stocks': top30_stocks})

# def last_trading_day(today):
#     if today.weekday() == 0:  # Monday
#         return today - timedelta(days=3)
#     elif today.weekday() == 6:  # Sunday
#         return today - timedelta(days=2)
#     else:
#         return today - timedelta(days=1)






# def update_table(request):
#     category = request.GET.get('category', '')  # 从请求中获取类别
#     stock_list = ... # 根据类别获取相应的股票数据

#     # 使用 render_to_string 渲染相应的模板。
#     thead_html = render_to_string('your_template_thead.html', {'category': category})
#     tbody_html = render_to_string('your_template_tbody.html', {'stock_list': stock_list})

#     return JsonResponse({'thead': thead_html, 'tbody': tbody_html})



# def get_last_trading_day(date):
#      # 將輸入日期轉換為weekday的索引（星期一為0，星期天為6）
#     weekday = date.weekday()
    
#     # 如果當日是星期一（0），減去3天回到上週五
#     if weekday == 0:
#         return date - timedelta(days=3)
#     # 如果當日是星期日（6），減去2天回到上週五
#     elif weekday == 6:
#         return date - timedelta(days=2)
#     # 其它情況，減去1天即為前一工作日
#     else:
#         return date - timedelta(days=1)

# def update_stocks_data():
#     # 检查缓存是否已经有数据
#     all_stocks_info = cache.get('all_stocks_info')

#     # 如果没有, 则从 twstock 獲取所有股票代碼資訊
#     if not all_stocks_info:
#         all_stocks_info = twstock.twse
#         # 轉換成字典
#         all_stocks_info = {k: v._asdict() for k, v in all_stocks_info.items()}
#         # 将得到的股票信息存入缓存，有效期设为1小时
#         cache.set('all_stocks_info', all_stocks_info, 60*60)

#     stock_codes = list(all_stocks_info.keys())

#      # 獲取今日日期
#     today = datetime.today().date()

#     # 前一個交易日
#     previous_trading_day = get_last_trading_day(today)
#     # previous_trading_day = get_last_trading_day(datetime.today().date())

#     for code in stock_codes:
#         time.sleep(0.1)
#         stock = twstock.Stock(code)
#         latest_data = stock.fetch_from(previous_trading_day.year, previous_trading_day.month)[0]

#         # 將撈取到的資料更新到資料庫中
#         PopularStock.objects.update_or_create(
#             stock_code=code,
#             defaults={
#                 'stock_name': all_stocks_info[code]['name'],
#                 'price': latest_data.close,
#                 'change': latest_data.change,
#                 'high': latest_data.high,
#                 'open': latest_data.open,
#                 'low': latest_data.low,
#                 'close': latest_data.close,
#                 'capacity': latest_data.capacity
#             })

# # 获取前一交易日成交量最多的前30名股票
# def get_top_30_stocks():
#     time.sleep(0.1)
#     # 尝试从缓存中获取
#     top_30_stocks = cache.get('top_30_stocks')

#     # 如果缓存中没有，则从数据库中撈出成交量最大的前30支股票，並存入緩存
#     if not top_30_stocks:
#         top_30_stocks = PopularStock.objects.all().order_by('-capacity')[:30]
#         # 将得到的股票信息存入缓存，有效期设为1小时
#         cache.set('top_30_stocks', top_30_stocks, 60*60)

#     return top_30_stocks

# def popular(request):
#     # 更新全部股票数据
#     update_stocks_data()

#     # 獲取成交量最多的前30名股票
#     top_30_stocks = get_top_30_stocks()
   
#     # 将结果传递至HTML模板中
#     return render(request, 'popular.html', {'top_30_stocks': top_30_stocks})