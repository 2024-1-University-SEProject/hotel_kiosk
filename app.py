from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
from datetime import datetime, timedelta
import jwt
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'
JWT_SECRET_KEY = 'hotel_kiosk_secure_key' # For JWT tokens

# Sample data for check-in/check-out process
guests = []
reservations = {}
reservation_counter = 1
a_receipts = []
a_rec_reservations = {}
call_records = []
roomnum = ''

# 객실 가격 데이터
room_prices_defalut = {
    '201': 50000, '202': 50000, '203': 50000, '204': 50000, '205': 50000, 
    '206': 50000, '207': 50000, '208': 50000, '209': 50000, '210': 50000, 
    '301': 70000, '302': 70000, '303': 70000, '304': 70000, '305': 70000, 
    '306': 70000, '307': 70000,
    '401': 100000, '402': 100000, '403': 100000, '404': 100000,
    '501': 200000, '502': 200000
}

room_prices = {
    '201': 50000, '202': 50000, '203': 50000, '204': 50000, '205': 50000, 
    '206': 50000, '207': 50000, '208': 50000, '209': 50000, '210': 50000, 
    '301': 70000, '302': 70000, '303': 70000, '304': 70000, '305': 70000, 
    '306': 70000, '307': 70000,
    '401': 100000, '402': 100000, '403': 100000, '404': 100000,
    '501': 200000, '502': 200000
}

room_states = {room: 'clean' for room in room_prices.keys()}

breakfast_price = 10000

# Language data
languages = {
    'ko': '한국어',
    'en': 'English',
    'zh': '中文'
}

# Default language
default_lang = 'ko'

def get_translations(lang):
    translations = {
            'ko': {
            'hotel_title': '나는야 호텔',
            'checkin': '체크인',
            'checkout': '체크아웃',
            'facilities': '시설 정보',
            'call_staff': '직원 호출/피드백',
            'name': '이름',
            'phone': '전화번호',
            'select_room': '객실 선택',
            'breakfast': '조식 여부',
            'payment_method': '결제 방식',
            'reservation_number': '예약 번호',
            'reservation_info': '예약 세부 정보',
            'pay': '결제',
            'confirm': '확인',
            'checkout_confirm': '체크아웃 확인',
            'checkout_complete': '체크아웃 완료되었습니다',
            'checkin_complete': '결제가 완료되었습니다',
            'all_fields_required': '모든 필드를 입력해 주세요.',
            'invalid_name': '체크인된 이름이 없습니다.',
            'room_is_dirty': '방이 청소되지 않았습니다. 관리자에게 문의하세요.',
            'invalid_name_or_room': '이름과 객실 번호가 일치하지 않습니다. 다시 입력해 주세요.',
            'room_already_checked_in': '해당 객실은 이미 체크인되었습니다. 다른 객실을 선택해 주세요.',
            'wifi_info': '와이파이 정보',
            'room_info': '객실 정보',
            'hotel_facilities': '호텔 층별 시설',
            'nearby_facilities': '호텔 주변 시설',
            'facility_info': '시설 정보',
            'built_by': '이 시설은 2024년 호텔 관리자에 의해 세워졌으며 앞으로 어떻게 될지 알 수 없습니다.',
            'call_reason': '호출 이유',
            'total_price': '총 금액',
            'wifi_name': '이름',
            'wifi_password': '비밀번호',
            'floor_info': '층 정보',
            'room_floor_info': '객실 정보',
            'kiosk_usage': '키오스크 이용',
            'room_change': '객실 변경',
            'customer_letter': '고객의 편지',
            'call_staff_title': '직원 호출/피드백',
            'admin': 'admin',
            'back': '뒤로 가기',
            'admin_dashboard': '관리자 대시보드',
            'admin_rates': '요금 설정',
            'admin_rooms': '룸 관리',
            'admin_services': '서비스 관리',
            'admin_reservations': '예약 관리',
            'admin_receipts': '현재 방 관리',
            'price_setting': '가격 설정',
            'room_number': '객실 번호',
            'price': '가격',
            'weekend_price_setting': '주말 요금 설정',
            'peak_season_price_setting': '성수기 요금 설정',
            'adjust_price': '전체 요금 설정',
            'admin_login' : '관리자 로그인',
            'admin_id' : '관리자 아이디',
            'admin_password' : '비밀번호',
            'admin_login_confirm' : '로그인',
            'admin_restore' : '영수증 관리',
            'admin_dirty_select': '방 선택',
            'admin_dirty_list' : '청소 안 된 방',
            'admin_dirty_clear' : '청소',
            'nowday': '날짜',
            'checkin_date': '체크인 시간',
            'checkout_date': '체크아웃 시간',
            'admin_receipt_info': '영수증',
            'admin_feedback': '피드백',
            'feedback_list': '피드백 리스트',
            'breakfast_is_good': '조식 맛있어요.',
            'breakfast_is_bad': '조식 맛없어요.',
            'service_is_good': '서비스 좋아요.',
            'service_is_bad': '서비스 별로에요.',
            'room_is_good': '방이 좋아요.',
            'room_is_bad': '방이 별로에요.',
            'b_p_setting': '조식 가격 설정',
            'b_price': '조식 가격',
            'b_p_changed': '조식 가격이 변경되었습니다.',
            'no_info_id': '예약 ID에 해당하는 정보가 없습니다.',
            'call_staff_complete':'전달되었습니다.',
            'room_cleaned': '방이 청소되었습니다.',
            'wrong_id': "잘못된 아이디 또는 비밀번호입니다.",
            'price_changed': '가격이 변경되었습니다.',
            'b_t_f_price': '전체 가격 초기화'
        },
            'en': {
            'hotel_title': 'I am Hotel',
            'checkin': 'Check-In',
            'checkout': 'Check-Out',
            'facilities': 'Facilities',
            'call_staff': 'Call Staff/Feedback',
            'name': 'Name',
            'phone': 'Phone Number',
            'select_room': 'Select Room',
            'breakfast': 'Breakfast',
            'payment_method': 'Payment Method',
            'reservation_number': 'Reservation Number',
            'reservation_info': 'Reservation Details',
            'pay': 'Pay',
            'confirm': 'Confirm',
            'checkout_confirm': 'Confirm Checkout',
            'checkout_complete': 'Checkout Complete',
            'checkin_complete': 'Payment Complete',
            'all_fields_required': 'Please fill in all fields.',
            'invalid_name': 'No check-in found for this name.',
            'room_is_dirty': 'The room has not been cleaned, please contact the manager.',
            'invalid_name_or_room': 'Name and room number do not match. Please try again.',
            'room_already_checked_in': 'The selected room is already checked in. Please choose another room.',
            'wifi_info': 'WiFi Information',
            'room_info': 'Room Information',
            'hotel_facilities': 'Hotel Facilities by Floor',
            'nearby_facilities': 'Nearby Facilities',
            'facility_info': 'Facility Information',
            'built_by': 'This facility was built in 2024 by Hotel Management and its future is uncertain.',
            'call_reason': 'Call Reason',
            'total_price': 'Total Price',
            'wifi_name': 'Name',
            'wifi_password': 'Password',
            'floor_info': 'Floor Information',
            'room_floor_info': 'Room Floor Information',
            'kiosk_usage': 'Kiosk Usage',
            'room_change': 'Room Change',
            'customer_letter': 'Customer Letter',
            'call_staff_title': 'Call Staff/Feedback',
            'admin': 'admin',
            'back': 'Back',
            'admin_dashboard': 'Admin Dashboard',
            'admin_rates': 'Set Rates',
            'admin_rooms': 'Manage Rooms',
            'admin_services': 'Manage Services',
            'admin_reservations': 'Manage Reservations',
            'admin_receipts': 'Current Room Status',
            'price_setting': 'Price Setting',
            'room_number': 'Room Number',
            'price': 'Price',
            'weekend_price_setting': 'Weekend Price Setting',
            'peak_season_price_setting': 'Peak Season Price Setting',
            'adjust_price': 'Adjust All Prices',
            'admin_login' : 'Admin Login',
            'admin_id' : 'admin id',
            'admin_password' : 'password',
            'admin_login_confirm' : 'login',
            'admin_restore' : 'Manage Receipts',
            'admin_dirty_select': 'Choose a room',
            'admin_dirty_list': 'Uncleaned Room',
            'admin_dirty_clear' : 'cleaning',
            'nowday': 'date',
            'checkin_date': 'checkin time',
            'checkout_date': 'checkout time',
            'admin_receipt_info': 'receipt',
            'admin_feedback': 'Feedback',
            'feedback_list': 'Feedback List',
            'breakfast_is_good': 'breakfast is good.',
            'breakfast_is_bad': 'breakfast is bad.',
            'service_is_good': 'service is good.',
            'service_is_bad': 'service is bad.',
            'room_is_good': 'room is good.',
            'room_is_bad': 'room is bad.',
            'b_p_setting': 'breakfast price setting',
            'b_price': 'breakfast price',
            'b_p_changed': 'The breakfast price has been changed.',
            'no_info_id': 'No information corresponding to reservation ID.',
            'call_staff_complete':'Complete',
            'room_cleaned': 'The room has been cleaned.',
            'wrong_id': "Invalid ID or password.",
            'price_changed': 'The price has been changed.',
            'b_t_f_price': 'Initialize all prices'
        },
            'zh': {
            'hotel_title': '我是酒店',
            'checkin': '入住',
            'checkout': '退房',
            'facilities': '设施',
            'call_staff': '呼叫工作人员/客户意见',
            'name': '姓名',
            'phone': '电话号码',
            'select_room': '选择房间',
            'breakfast': '早餐',
            'payment_method': '付款方式',
            'reservation_number': '预约号码',
            'reservation_info': '预约详细信息',
            'pay': '付款',
            'confirm': '确认',
            'checkout_confirm': '确认退房',
            'checkout_complete': '退房完成',
            'checkin_complete': '付款完成',
            'all_fields_required': '请填写所有字段。',
            'invalid_name': '没有找到该名称的入住记录。',
            'room_is_dirty': '房间没有打扫。 请咨询管理员。',
            'invalid_name_or_room': '姓名和房间号不匹配，请重试。',
            'room_already_checked_in': '所选房间已办理入住。请选择其他房间。',
            'wifi_info': 'WiFi 信息',
            'room_info': '房间信息',
            'hotel_facilities': '酒店设施',
            'nearby_facilities': '附近设施',
            'facility_info': '设施信息',
            'built_by': '此设施由酒店经理于2024年建成，未来充满不确定性。',
            'call_reason': '呼叫原因',
            'total_price': '总价格',
            'wifi_name': '名称',
            'wifi_password': '密码',
            'floor_info': '楼层信息',
            'room_floor_info': '房间楼层信息',
            'kiosk_usage': '使用自助服务终端',
            'room_change': '房间更换',
            'customer_letter': '客户信',
            'call_staff_title': '呼叫工作人员/客户意见',
            'admin': 'admin',
            'back': '后退',
            'admin_dashboard': '管理员仪表板',
            'admin_rates': '设置费率',
            'admin_rooms': '管理房间',
            'admin_services': '管理服务',
            'admin_reservations': '管理预订',
            'admin_receipts': '当前房间现状',
            'price_setting': '价格设定',
            'room_number': '房间号',
            'price': '价格',
            'weekend_price_setting': '周末价格设定',
            'peak_season_price_setting': '旺季价格设定',
            'adjust_price': '调整所有价格',
            'admin_login' : '管理员登录',
            'admin_id' : '邮箱',
            'admin_password' : '密码',
            'admin_login_confirm' : '注册',
            'admin_restore' : '管理收据',
            'admin_dirty_select' : '选择房间',
            'admin_dirty_list':"没有打扫的房间",
            'admin_dirty_clear': '打扫',
            'nowday': '日期',
            'checkin_date': '入住时间',
            'checkout_date': '退房时间',
            'admin_receipt_info': '收据',
            'admin_feedback': '客户意见',
            'feedback_list': '意见表',
            'breakfast_is_good': '早餐很好吃。',
            'breakfast_is_bad': '早餐不好吃。',
            'service_is_good': '服务很好。',
            'service_is_bad': '服务不好。',
            'room_is_good': '房间很好。',
            'room_is_bad': '房间不好。',
            'b_p_setting': '早餐价格设定',
            'b_price': '早餐价格',
            'b_p_changed': '早餐的价格变更了。',
            'no_info_id': '预约ID相应的信息不存在。',
            'call_staff_complete':'已转发。',
            'room_cleaned': '房间打扫了。',
            'wrong_id': "ID或密码错误。",
            'price_changed': '价格变更了。',
            'b_t_f_price': '重置全部价格'
        }
    }
    return translations.get(lang, translations[default_lang])

# --- JWT Utility Functions ---
def create_jwt(user_info):
    payload = {
        'user_info': user_info,
        'exp': datetime.utcnow() + timedelta(hours=2)
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_info']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('admin_token')
        if not token:
            return redirect(url_for('admin_login', lang=request.args.get('lang', default_lang)))
        
        user_info = decode_jwt(token)
        if not user_info or user_info.get('role') != 'admin':
            return redirect(url_for('admin_login', lang=request.args.get('lang', default_lang)))
        
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('users/index.html', translations=translations, languages=languages, current_lang=lang)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin1234':
            user_info = {'username': 'admin', 'role': 'admin'}
            token = create_jwt(user_info)
            
            response = make_response(redirect(url_for('admin_dashboard', lang=lang)))
            response.set_cookie('admin_token', token, httponly=True)
            return response
        else:
            flash(translations['wrong_id'])
    
    return render_template('admin/login.html', translations=translations, languages=languages, current_lang=lang)

@app.route('/admin/dashboard')
@token_required
def admin_dashboard():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('admin/dashboard.html', translations=translations, languages=languages, current_lang=lang)

@app.route('/admin/price', methods=['GET', 'POST'])
@token_required
def admin_price():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    
    if request.method == 'POST':
        room_number = request.form['room_number']
        price = request.form['price']
        if room_number in room_prices:
            room_prices[room_number] = int(price)
            flash(f"{translations['room_number']} {room_number} {translations['price']} {price} {translations['confirm']}")
        else:
            flash(f"{translations['invalid_name']}")
    
    return render_template('admin/price.html', translations=translations, languages=languages, current_lang=lang, room_prices=room_prices)

@app.route('/admin/adjust_price')
@token_required
def adjust_price():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('admin/adjust_price.html', translations=translations, current_lang=lang)

@app.route('/admin/adjust_price/weekend', methods=['GET', 'POST'])
@token_required
def adjust_weekend_price():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    if request.method == 'POST':
        adjustment = int(request.form['adjustment'])
        for room in room_prices:
            room_prices[room] += adjustment
        flash(translations['price_changed'])
    return render_template('admin/weekend_price.html', translations=translations, current_lang=lang)

@app.route('/admin/adjust_price/back_to_first_price', methods=['GET', 'POST'])
@token_required
def adjust_back_to_first_price():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    if request.method == 'POST':
        for room in room_prices:
            room_prices[room] = room_prices_defalut[room]
        flash(translations['price_changed'])
    return render_template('admin/back_to_first_price.html', translations=translations, current_lang=lang)

@app.route('/admin/dirty_rooms')
@token_required
def dirty_rooms():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    dirty_rooms = {room: price for room, price in room_prices.items() if room_states[room] == 'dirty'}
    return render_template('admin/dirty_rooms.html', translations=translations, current_lang=lang, dirty_rooms=dirty_rooms)

@app.route('/admin/clean_room', methods=['POST'])
@token_required
def clean_room():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    room_number = request.form['room_number']
    if room_number in room_states:
        room_states[room_number] = 'clean'
        flash(translations['room_cleaned'])
    return redirect(url_for('dirty_rooms', lang=lang))

@app.route('/admin/receipts')
@token_required
def admin_receipts():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('admin/receipts.html', translations=translations, reservations=reservations, current_lang=lang, guests=guests)

@app.route('/admin/receipts/<int:reservation_number>')
@token_required
def receipt_details(reservation_number):
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    guest = next((g for g in guests if g['reservation_number'] == reservation_number), None)
    a_receipt = next((g for g in a_receipts if g['reservation_number'] == reservation_number), None)
    if not a_receipt:
        flash(translations['no_info_id'])
        return redirect(url_for('admin_receipts', lang=lang))
    return render_template('admin/receipt_details.html', translations=translations, current_lang=lang, a_receipt=a_receipt)


@app.route('/admin/restore')
@token_required
def admin_restore():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('admin/restore.html', translations=translations, reservations=reservations, a_rec_reservations=a_rec_reservations, current_lang=lang, guests=guests)

@app.route('/admin/restore/<int:reservation_number>')
@token_required
def restore_details(reservation_number):
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    a_receipt = next((g for g in a_receipts if g['reservation_number'] == reservation_number), None)
    print(a_receipt)
    if not a_receipt:
        flash(translations['no_info_id'])
        return redirect(url_for('admin_restore', lang=lang))
    return render_template('admin/restore_details.html', translations=translations, current_lang=lang, a_receipt=a_receipt)

@app.route('/admin/adjust_price/breakfast', methods=['GET', 'POST'])
@token_required
def adjust_breakfast_price():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    global breakfast_price
    if request.method == 'POST':
        breakfast_price = int(request.form['breakfast_price'])
        flash(translations['b_p_changed'])
        return redirect(url_for('adjust_price', lang=lang))
    return render_template('admin/breakfast_price.html', translations=translations, current_lang=lang)

@app.route('/admin/feedback')
@token_required
def feedback():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('admin/feedback.html', call_records=call_records, translations=translations, current_lang=lang)

@app.route('/admin/logout')
def admin_logout():
    lang = request.args.get('lang', default_lang)
    response = make_response(redirect(url_for('admin_login', lang=lang)))
    response.set_cookie('admin_token', '', expires=0)
    return response


#///////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/users/facilities')
def facilities():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    return render_template('users/facilities.html', translations=translations, languages=languages, current_lang=lang)


@app.route('/users/call_staff', methods=['GET', 'POST'])
def call_staff():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    
    if request.method == 'POST':
        reason = request.form['reason']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        call_records.append({'timestamp': timestamp, 'reason': reason})
        flash(translations['call_staff_complete'])
        return redirect(url_for('call_staff', lang=lang))
    
    return render_template('users/call_staff.html', translations=translations, languages=languages, current_lang=lang)

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    global roomnum
    room_priceses = roomnum
    if request.method == 'POST':
        global reservation_counter
        name = request.form['name']
        phone = request.form['phone']
        room = roomnum
        # 이미 체크인된 객실인지 확인
        if any(guest['room'] == room for guest in guests):
            flash(translations['room_already_checked_in'])
            return redirect(url_for('checkin', lang=lang))
        if room_states[room] == 'dirty':
            flash(translations['room_is_dirty'])
            return redirect(url_for('checkin', lang=lang))
        breakfast = request.form['breakfast']
        payment = request.form['payment']
        price = room_prices[room] + (breakfast_price if breakfast == 'Yes' else 0)
        reservation_number = reservation_counter
        reservation_counter += 1
        now_day = datetime.now() + timedelta(days=1)
        checkout_day = datetime(now_day.year, now_day.month, now_day.day, 12, 0, 0)
        guests.append({'name': name, 'phone': phone, 'room': room, 'breakfast': breakfast, 'payment': payment, 'price': price, 'reservation_number': reservation_number})
        a_receipts.append({'name': name, 'phone': phone, 'room': room, 'breakfast': breakfast, 'payment': payment, 'price': price, 'reservation_number': reservation_number, 'date': datetime.now(), 'checkout_day': checkout_day})
        reservations[reservation_number] = name
        a_rec_reservations[reservation_number] = name
        session['guest'] = guests[-1]
        
        # --- JWT Issue for Guest ---
        guest_info = {'name': name, 'phone': phone, 'room': room, 'reservation_number': reservation_number, 'role': 'guest'}
        token = create_jwt(guest_info)
        
        response = make_response(redirect(url_for('checkin_confirm', lang=lang)))
        response.set_cookie('guest_token', token, httponly=True)
        return response
    return render_template('users/checkin.html', translations=translations, languages=languages, room_prices=room_prices, breakfast_price=breakfast_price, room_priceses=room_priceses, current_lang=lang)

@app.route('/select_room', methods=['GET', 'POST'])
def select_room():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    if request.method == 'POST':
        room = request.form['room']
        global roomnum
        roomnum = room
        if any(guest['room'] == room for guest in guests):
            flash(translations['room_already_checked_in'])
            return redirect(url_for('select_room', lang=lang))
        if room_states[room] == 'dirty':
            flash(translations['room_is_dirty'])
            return redirect(url_for('select_room', lang=lang))
        return redirect(url_for('checkin', lang=lang))
    
    available_rooms = {room: price for room, price in room_prices.items() if room_states[room] == 'clean'}
    return render_template('users/select_room.html', translations=translations, available_rooms=available_rooms, room_prices=room_prices, current_lang=lang)



@app.route('/checkin_confirm', methods=['GET', 'POST'])
def checkin_confirm():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    guest = session.get('guest')
    if request.method == 'POST':
        flash(translations['checkin_complete'])
        return redirect(url_for('index', lang=lang))
    return render_template('users/checkin_confirm.html', translations=translations, languages=languages, guest=guest, current_lang=lang)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    
    # --- JWT Verification for Guest ---
    guest_from_token = None
    token = request.cookies.get('guest_token')
    if token:
        guest_from_token = decode_jwt(token)

    if request.method == 'POST':
        name = request.form['name']
        reservation_number = int(request.form['reservation_number'])
        if reservation_number in reservations and reservations[reservation_number] == name:
            guest = next((g for g in guests if g['reservation_number'] == reservation_number), None)
            if guest:
                room_states[guest['room']] = 'dirty'  # Mark the room as dirty            
                session['guest'] = guest
                return redirect(url_for('checkout_confirm', lang=lang))
        flash(translations['invalid_name_or_room'])
    return render_template('users/checkout.html', translations=translations, languages=languages, current_lang=lang, guest_from_token=guest_from_token)

@app.route('/checkout_confirm', methods=['GET', 'POST'])
def checkout_confirm():
    lang = request.args.get('lang', default_lang)
    translations = get_translations(lang)
    guest = session.get('guest')
    if request.method == 'POST':
        guests.remove(guest)
        del reservations[guest['reservation_number']]
        flash(translations['checkout_complete'])
        
        response = make_response(redirect(url_for('index', lang=lang)))
        response.set_cookie('guest_token', '', expires=0) # Logout guest
        return response
    return render_template('users/checkout_confirm.html', translations=translations, languages=languages, guest=guest, current_lang=lang)

def calculate_price(room, breakfast):
    price = room_prices.get(room, 0)
    if breakfast == 'Yes':
        price += breakfast_price
    return price

if __name__ == '__main__':
    app.run(debug=True)
