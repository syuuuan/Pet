import streamlit as st
import datetime

# 設定網頁為寬版佈局
st.set_page_config(layout="wide", page_title="流浪寵物領養系統 V2", page_icon="🐾")

st.title("🐾 流浪寵物領養系統 ")
st.markdown("---")

# 定義台灣行政區資料庫（用於聯動選單）
TAIWAN_LOCATIONS = {
    "基隆市": ["中正區", "七堵區", "暖暖區", "仁愛區", "中山區", "安樂區", "信義區"],
    "臺北市": ["中正區", "大同區", "中山區", "松山區", "大安區", "萬華區", "信義區", "士林區", "北投區", "內湖區", "南港區", "文山區"],
    "新北市": ["板橋區", "三重區", "中和區", "永和區", "新莊區", "新店區", "樹林區", "鶯歌區", "三峽區", "淡水區", "汐止區", "瑞芳區", "土城區", "蘆洲區", "五股區", "泰山區", "林口區", "深坑區", "石碇區", "坪林區", "三芝區", "石門區", "八里區", "平溪區", "雙溪區", "貢寮區", "金山區", "萬里區", "烏來區"],
    "桃園市": ["桃園區", "中壢區","大溪區", "楊梅區", "蘆竹區" , "大園區", "龜山區" , "八德區" , "龍潭區" , "平鎮區", "新屋區" , "觀音區" , "復興區"],
    "新竹市": ["東區", "北區", "香山區"],
    "新竹縣": ["竹北市", "竹東鎮", "新埔鎮", "關西鎮", "湖口鄉", "新豐鄉", "芎林鄉", "橫山鄉", "北埔鄉", "寶山鄉", "峨眉鄉", "尖石鄉", "五峰鄉"],
    "苗栗縣": ["苗栗市", "苑裡鎮", "通霄鎮", "竹南鎮", "頭份市", "後龍鎮", "卓蘭鎮", "大湖鄉", "公館鄉", "銅鑼鄉", "南庄鄉", "頭屋鄉", "三義鄉", "西湖鄉", "造橋鄉", "三灣鄉", "獅潭鄉", "泰安鄉"],
    "臺中市": ["中區", "東區", "南區", "西區", "北區", "北屯區", "西屯區", "南屯區", "北屯區", "豐原區", "東勢區", "大甲區", "清水區", "沙鹿區", "梧棲區", "后里區", "神岡區", "潭子區", "大雅區", "新社區", "石岡區", "外埔區", "大安區", "烏日區", "大肚區", "龍井區", "霧峰區", "太平區", "大里區", "和平區"],
    "彰化縣": ["彰化市", "鹿港鎮", "和美鎮", "線西鄉", "伸港鄉", "福興鄉", "秀水鄉", "花壇鄉", "芬園鄉", "員林市", "溪湖鎮", "田中鎮", "大村鄉", "埔鹽鄉", "埔心鄉", "永靖鄉", "社頭鄉", "二水鄉", "北斗鎮", "二林鎮", "田尾鄉", "埤頭鄉", "芳苑鄉", "大城鄉", "竹塘鄉", "溪州鄉"],
    "南投縣": ["南投市", "埔里鎮", "草屯鎮 ", "竹山鎮", "集集鎮", "名間鄉", "鹿谷鄉", "中寮鄉", "魚池鄉", "國姓鄉", "水里鄉", "信義鄉", "仁愛鄉"],
    "雲林縣": ["斗六市", "斗南鎮", "虎尾鎮", "西螺鎮", "土庫鎮", "北港鎮", "古坑鄉", "大埤鄉", "莿桐鄉", "林內鄉", "二崙鄉", "崙背鄉", "麥寮鄉", "東勢鄉", "褒忠鄉", "臺西鄉", "元長鄉", "四湖鄉", "口湖鄉", "水林鄉"],
    "嘉義縣": ["太保市", "朴子市", "布袋鎮", "大林鎮", "民雄鄉", "溪口鄉", "新港鄉", "六腳鄉", "東石鄉", "義竹鄉", "鹿草鄉", "水上鄉", "中埔鄉", "竹崎鄉", "梅山鄉", "番路鄉", "大埔鄉", "阿里山鄉"],
    "嘉義市": ["東區", "西區"],
    "臺南市": ["新營區", "鹽水區", "白河區", "柳營區", "後壁區", "東山區", "麻豆區", "下營區", "六甲區", "官田區", "大內區", "佳里區", "學甲區", "西港區", "七股區", "將軍區", "北門區", "新化區", "善化區", "新市區", "安定區", "山上區", "玉井區", "楠西區", "南化區", "左鎮區", "仁德區", "歸仁區", "關廟區", "龍崎區", "永康區", "東區", "南區", "北區", "安南區", "安平區", "中西區"],
    "高雄市": ["鹽埕區", "鼓山區", "左營區", "楠梓區", "三民區", "新興區", "前金區", "苓雅區", "前鎮區", "旗津區", "小港區", "鳳山區", "林園區", "大寮區", "大樹區", "大社區", "仁武區", "鳥松區", "岡山區", "橋頭區", "燕巢區", "田寮區", "阿蓮區", "路竹區", "湖內區", "茄萣區", "永安區", "彌陀區", "梓官區","旗山區", "美濃區", "六龜區", "甲仙區", "杉林區", "內門區", "茂林區", "桃源區", "那瑪夏區"],
    "屏東縣": ["屏東市", "潮州鎮", "東港鎮", "恆春鎮", "萬丹鄉", "長治鄉", "麟洛鄉", "麟洛鄉", "里港鄉", "鹽埔鄉", "高樹鄉", "萬巒鄉", "內埔鄉", "竹田鄉", "新埤鄉", "枋寮鄉", "新園鄉 ", "崁頂鄉", "林邊鄉", "南州鄉", "佳冬鄉", "琉球鄉", "車城鄉", "滿州鄉", "枋山鄉", "三地門鄉", "霧臺鄉", "瑪家鄉", "泰武鄉", "來義鄉", "春日鄉", "獅子鄉", "牡丹鄉"],
    "宜蘭縣": ["宜蘭市", "羅東鎮", "蘇澳鎮", "頭城鎮", "礁溪鄉", "壯圍鄉", "員山鄉", "冬山鄉", "五結鄉", "三星鄉", "大同鄉", "南澳鄉"],
    "花蓮縣": ["花蓮市", "鳳林鎮", "玉里鎮", "新城鄉", "吉安鄉", "壽豐鄉", "光復鄉", "豐濱鄉", "瑞穗鄉", "富里鄉", "秀林鄉", "萬榮鄉", "卓溪鄉"],
    "臺東縣": ["臺東市", "成功鎮", "關山鎮", "卑南鄉", "鹿野鄉", "池上鄉", "東河鄉", "長濱鄉", "太麻里鄉", "大武鄉", "綠島鄉", "海端鄉", "延平鄉", "金峰鄉", "達仁鄉", "蘭嶼鄉"],
    "澎湖縣": ["馬公市", "湖西鄉", "白沙鄉", "西嶼鄉", "望安鄉", "七美鄉"],
    "連江縣": ["南竿鄉", "北竿鄉", "莒光鄉", "東引鄉"],
    "金門縣": ["金城鎮", "金沙鎮", "金湖鎮", "金寧鄉", "烈嶼鄉", "烏坵鄉"]
}

# --- 初始化系統暫存庫 ---
if "pets" not in st.session_state:
    st.session_state.pets = [
        {
            "id": 1, "type": "狗", "breed": "柴犬", "photo": None, "features": "親人、會坐下、脖子有藍色項圈",
            "city": "臺北市", "district": "大安區", "date": datetime.date(2026, 6, 1),
            "finder_name": "阿明", "finder_phone": "0912345678", "status": "開放領養"
        },
        {
            "id": 2, "type": "貓", "breed": "橘貓", "photo": None, "features": "愛叫、左耳已剪耳、微胖",
            "city": "高雄市", "district": "三民區", "date": datetime.date(2026, 6, 15),
            "finder_name": "小紅", "finder_phone": "0987-654321", "status": "開放領養"
        }
    ]
if "id_counter" not in st.session_state: st.session_state.id_counter = 3
if "uploader_key" not in st.session_state: st.session_state.uploader_key = 0
if "msg_success" not in st.session_state: st.session_state.msg_success = ""
if "msg_error" not in st.session_state: st.session_state.msg_error = ""

# --- ✨ 核心修正：將「提交」動作寫在 Callback 函式中，絕對不卡鍵 ---
def handle_pet_submit():
    # 從 Session State 抓取目前畫面上填寫的值
    p_type = st.session_state.get("ins_type", "").strip()
    p_breed = st.session_state.get("ins_breed", "").strip()
    
    if not p_type or not p_breed:
        st.session_state.msg_error = "❌ 請填寫必要欄位（種類、品種）！"
        st.session_state.msg_success = ""
        return
        
    # 打包新增到資料庫
    new_pet = {
        "id": st.session_state.id_counter,
        "type": p_type,
        "breed": p_breed,
        "photo": st.session_state.get(f"ins_photo_{st.session_state.uploader_key}"),
        "features": st.session_state.get("ins_features", ""),
        "city": st.session_state.get("ins_city"),         
        "district": st.session_state.get("ins_district"), 
        "date": st.session_state.get("ins_date"),
        "finder_name": st.session_state.get("ins_name", ""),
        "finder_phone": st.session_state.get("ins_phone", ""),
        "status": "開放領養"
    }
    st.session_state.pets.append(new_pet)
    st.session_state.id_counter += 1
    st.session_state.msg_success = f"🎉 成功新增一筆 {p_type}({p_breed}) 的流浪寵物資訊！"
    st.session_state.msg_error = ""
    
    # 📝 安全清空所有輸入格
    st.session_state.ins_type = ""
    st.session_state.ins_breed = ""
    st.session_state.ins_features = ""
    st.session_state.ins_name = ""
    st.session_state.ins_phone = ""
    # 變更圖片組件的 Key，使其強制歸零清空
    st.session_state.uploader_key += 1

# 建立左右兩邊的系統區塊
col1, col2 = st.columns(2)

# ==================== 左邊系統：管理與新增 ====================
with col1:
    st.header("🛠️ 管理與新增系統")
    
    with st.container(border=True):
        st.subheader("➕ 新增流浪寵物資訊")
        
        # 綁定 key 供後台 callback 使用
        st.text_input("種類（例如：狗、貓、鳥）*", key="ins_type")
        st.text_input("品種*", key="ins_breed")
        
        # 使用動態 Key，上傳完畢送出後會自動清空照片
        st.file_uploader("上傳照片", type=["jpg", "jpeg", "png"], key=f"ins_photo_{st.session_state.uploader_key}")
        st.text_area("特徵說明", placeholder="請輸入外觀特徵或健康狀況...", key="ins_features")
        
        # --- 📍 地區即時聯動選單（完全獨立，點選縣市立刻更新區域） ---
        st.write("**📍 拾獲地點選取**")
        form_city = st.selectbox("請選擇縣市", list(TAIWAN_LOCATIONS.keys()), key="ins_city")
        form_district = st.selectbox("請選擇區域：", TAIWAN_LOCATIONS[form_city], key="ins_district")
        
        st.date_input("拾獲日期", value=datetime.date.today(), key="ins_date")
            
        st.markdown("**【拾獲者聯絡方式】**")
        st.text_input("暱稱", key="ins_name")
        st.text_input("電話", key="ins_phone")
        
        # 🎯 綁定 on_click 函式，點擊時立刻觸發安全儲存與清空
        st.button("提交新增資訊", type="primary", on_click=handle_pet_submit)
        
        # 顯示提交結果訊息
        if st.session_state.msg_error:
            st.error(st.session_state.msg_error)
        if st.session_state.msg_success:
            st.success(st.session_state.msg_success)

    st.markdown("---")
    st.subheader("⚙️ 現有資訊狀態調整 / 刪除")
    
    if not st.session_state.pets:
        st.info("目前系統內沒有寵物資料。")
    else:
        for i, pet in enumerate(st.session_state.pets):
            status_color = "🟢" if pet["status"] == "開放領養" else "🔴"
            with st.container(border=True):
                st.write(f"**{status_color} [{pet['type']}] {pet['breed']}**")
                st.write(f"📍 地點: {pet['city']}{pet['district']} | 📅 日期: {pet['date']}")
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if pet["status"] == "開放領養":
                        if st.button("標記為 [已被領養]", key=f"adopt_{pet['id']}"):
                            st.session_state.pets[i]["status"] = "已被領養"
                            st.rerun()
                    else:
                        if st.button("恢復為 [開放領養]", key=f"reopen_{pet['id']}"):
                            st.session_state.pets[i]["status"] = "開放領養"
                            st.rerun()
                with btn_col2:
                    if st.button("🗑️ 刪除整篇資訊", key=f"delete_{pet['id']}", type="primary"):
                        st.session_state.pets.pop(i)
                        st.rerun()


# ==================== 右邊系統：查看與搜尋 ====================
with col2:
    st.header("🔍 瀏覽與搜尋領養資訊")
    
    if not st.session_state.pets:
        st.info("目前系統內沒有任何寵物資料可供查詢。")
    else:
        st.subheader("🎛️ 綜合篩選器")
        
        existing_types = sorted(list(set(pet["type"] for pet in st.session_state.pets)))
        
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            search_type = st.selectbox("1. 選擇寵物種類：", ["全部種類"] + existing_types)
            
            if search_type != "全部種類":
                existing_breeds = sorted(list(set(pet["breed"] for pet in st.session_state.pets if pet["type"] == search_type)))
            else:
                existing_breeds = sorted(list(set(pet["breed"] for pet in st.session_state.pets)))
                
            search_breed = st.selectbox("2. 選擇品種：", ["全部品種"] + existing_breeds)
            
        with filter_col2:
            search_city = st.selectbox("3. 篩選縣市：", ["全部縣市"] + list(TAIWAN_LOCATIONS.keys()))
            
            if search_city != "全部縣市":
                search_district = st.selectbox("4. 篩選區域：", ["全部區域"] + TAIWAN_LOCATIONS[search_city])
            else:
                search_district = "全部區域"
                
        # --- 篩選邏輯核心 ---
        filtered_pets = st.session_state.pets
        
        if search_type != "全部種類":
            filtered_pets = [p for p in filtered_pets if p["type"] == search_type]
            
        if search_breed != "全部品種":
            filtered_pets = [p for p in filtered_pets if p["breed"] == search_breed]
            
        if search_city != "全部縣市":
            filtered_pets = [p for p in filtered_pets if p["city"] == search_city]
            
        if search_district != "全部區域":
            filtered_pets = [p for p in filtered_pets if p["district"] == search_district]
            
        # --- 顯示結果 ---
        st.markdown(f"📊 搜尋結果：共找到 **{len(filtered_pets)}** 筆符合條件的資料")
        st.markdown("---")
        
        if not filtered_pets:
            st.warning(" 找不到符合目前篩選條件的寵物，請嘗試放寬篩選條件。")
        else:
            st.caption("💡 點擊下方項目可展開查看完整詳細資訊與聯絡方式")
            
            for pet in filtered_pets:
                badge = "【開放中】" if pet["status"] == "開放領養" else "【已被領養】"
                title_text = f"{badge} 種類:{pet['type']} ｜ 品種:{pet['breed']} ｜ 特徵:{pet['features'][:10]}... ｜ 地點:{pet['city']}{pet['district']} ｜ 日期:{pet['date']}"
                
                with st.expander(title_text):
                    st.write(f"**🐾 寵物種類：** {pet['type']}")
                    st.write(f"**🧬 寵物品種：** {pet['breed']}")
                    st.write(f"**📌 目前狀態：** {pet['status']}")
                    st.write(f"**📍 拾獲地點：** {pet['city']}{pet['district']}")
                    st.write(f"**📅 拾獲日期：** {pet['date']}")
                    st.write(f"**✨ 完整特徵：** {pet['features'] if pet['features'] else '無'}")
                    
                    if pet["photo"] is not None:
                        st.image(pet["photo"], caption=f"{pet['breed']} 的照片", use_container_width=True)
                    else:
                        st.caption("（這隻寵物沒有上傳照片）")
                        
                    st.markdown("---")
                    st.markdown("**📞 拾獲者聯絡資訊**")
                    st.write(f"👤 **暱稱：** {pet['finder_name'] if pet['finder_name'] else '未提供'}")
                    st.write(f"📱 **電話：** {pet['finder_phone'] if pet['finder_phone'] else '未提供'}")
