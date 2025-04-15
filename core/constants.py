MODEL_ICONS = {
    "province": "🗺️",  # STM Bağlı İl Kodları
    "transactiontype": "🔄",  # İşlem Niteliği Kodları
    "port": "⚓",  # Uluslararası Liman Kodları
    "paymentmethod": "💳",  # Ödeme Şekilleri
    "additionalinfocode": "ℹ️",  # Tamamlayıcı Bilgi Kodları
    "antidumpingcompany": "🏭",  # Anti-Damping Vergisi
    "customsoffice": "🏢",  # Gümrük İdareleri
    "transportvehicle": "🚚",  # Taşıma Araçları
    "internationalagreement": "🌍",  # Uluslararası Anlaşmalar
    "simplifiedprocedure": "⚙️",  # Basitleştirilmiş Usul
    "harbor": "🚢",  # Limanlar
    "measurementunit": "📏",  # Ölçü Birimleri
    "exemptioncode": "🚫",  # Muafiyet Kodları
    "requireddocument": "📄",  # İstenen Dökümanlar
    "airport": "✈️",  # Havalimanları
    "airlinecompany": "🛫",  # Uçak Şirketleri
    "deliverymethod": "📦",  # Teslim Şekilleri
    "taxcode": "💰",  # Güncel Vergi Kodları
    "transporttype": "🛤️",  # Taşıma Türleri
    "containercode": "📦",  # Kap Kodları
    "currencytype": "💱",  # Döviz Cinsi
    "country": "🌎",  # Ülke Kodları
    "regimecode": "⚖️",  # Rejim Kodları
    "warehouse": "🏬",  # Ambar Kodları
    "depot": "🏠",  # Antrepo Kodları
    "bank": "🏦",  # Bankalar
    "city": "🏙️",  # Şehir
    "paymenttype": "💵",  # ödeme tipi
    "customstype": "🛃",
    "chiefcustomsoffice": "🏛️",
    "quantitytype": "📏",
    "customertype": "👥",
    "bankbranches": "🏢",  # Banka Şubeleri
    "brand": "🏷️",
    "productmodel": "🗂️",
    "uploadeddocuments": "📎",  # Yüklenen Belgeler
    "products": "🛍️",  # Ürünler
    "gtipcode": "📑",  # GTİP Kodları
}

# core/constants.py
MODEL_FIELD_VERBOSE_NAMES = {
    'country': {
        'country_code_alpha2': 'Ülke Kodu (Alpha-2)',
        'country_code_alpha3': 'Ülke Kodu (Alpha-3)',
        'country_name_tr': 'Ülke Adı (TR)',
        'country_name_en': 'Ülke Adı (EN)',
        'country_number': 'Ülke Numarası',
        'country_lang_code': 'Dil Kodu',
        'country_phone_code': 'Telefon Kodu',
        'currency_id': 'Para Birimleri',
    },
    'currencytype': {
        'currency_code_3_alpha': 'Para Birimi Kodu',
        'name': 'Para Birimi Adı(EN)',
        'code' : 'Para Birimi Numarası',
        'minor_unit' : 'Alt Birim',
        'name_tr' : 'Para Birimi Adı'
    },
    'city': {
        'code': 'Kodu',
        'name': 'Adı',
        'country_id': 'Ülke Adı',
        'state': 'Eyalet',
    },

    'paymentmethod': {
        'code': 'Kodu',
        'name': 'Adı',
        'description': 'Açıklama',
        'risk_status': 'Risk Durumu',
        'usage_status': 'Kullanım Sıklığı',
        'edi_code': 'EDİ Kodu'
    },

    'paymenttype': {
        'code': 'Kodu',
        'name': 'Adı',
        'description': 'Açıklama',
        'risk_status': 'Risk Durumu',
        'usage_status': 'Kullanım Sıklığı',
        'edi_code': 'EDİ Kodu'
    },
    'customstype': {
        'code': 'Kodu',
        'name': 'Adı',
        'description': 'Açıklama',

    },
    'chiefcustomsoffice': {
        'code': 'Kodu',
        'name': 'Adı',
        'code_accountancy': 'Saymanlık Kodu',
        'name_accountancy': 'Saymanlık Adı'

    },

    'customsoffice': {
        'code': 'Gümrük Kodu',
        'name': 'Gümrük Adı',
        'customs_type_id': 'Gümrük Tipi',
        'chief_customs_id': 'Üst Müdürlük Kodu',
        'city_id': 'Şehir'
    },
    'port': {

        'code': 'Kodu',
        'name': 'Adı',
        'country_id': 'Ülke'
    },
    'requireddocument': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'edi_code': "Edi Kodu"
    },
    'deliverymethod': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',

    },
    'airport': {
        'code_iata': 'IATA Kodu',
        'code_icao': 'ICAO Kodu',
        'city_id': 'Yerleşim',
        'country_id': 'Ülke',
        'name': 'Adı',
        'latitude_degree': 'Enlem',
        'longitude_degree': 'Boylam'
    },
    'taxcode': {

        'code': 'Kodu',
        'name': 'Adı',
        'tax_ratio': 'Oranı(%)',

    },

    'transporttype': {

        'code': 'Kodu',
        'name_tr': 'Adı',
        'name_en': 'Adı(EN)',
        'edi_code': "EDİ Kodu",
        "e_invoice_code": 'E-Fatura Kodu'

    },
    'containercode': {

        'code': 'Kodu',
        'name': 'Adı',
    },
    'quantitytype': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'edi_code': "EDİ Kodu",
    },

    'bank': {
        'swift_code': 'Swift Kodu',
        'bank_name': 'Adı',
        'address': 'Adres',
        'eft_number': 'EFT Numarası',
        'bank_logo': 'Logo'

    },
    'customertype': {

        'code': 'Kodu',
        'name': 'Adı',
    },
    'bankbranches': {

        'bank_id': 'Banka',
        'name': 'Şube Adı',
        'branches_code' : 'Şube Kodu',
        'city_id' : 'Şehir'
    },
}

# constants.py
FK_M2M_REPRESENTATIVE_FIELDS = {
    "Country": "country_name_tr",
    "City": "name",
    "CurrencyType": "name_tr",
    "ChiefCustomsOffice": "code",
    "CustomsType": "code",
    "Bank": 'bank_name'
}
