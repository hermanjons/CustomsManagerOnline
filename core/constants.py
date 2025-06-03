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
    "datasource": "🧩",  # Veri Kaynağı
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
        'currency': 'Para Birimleri',
        'data_source': 'Veri Kaynağı'
    },
    'currencytype': {
        'currency_code_3_alpha': 'Para Birimi Kodu',
        'name': 'Para Birimi Adı(EN)',
        'code': 'Para Birimi Numarası',
        'minor_unit': 'Alt Birim',
        'name_tr': 'Para Birimi Adı',
        'data_source': 'Veri Kaynağı'
    },
    'city': {
        'code': 'Kodu',
        'name': 'Adı',
        'country': 'Ülke Adı',
        'up_city': 'Üst Yerleşim',
        'capitol_city': 'Başkent',
        'data_source': 'Veri Kaynağı',
        'name_alternate': 'Alternatif Adı'
    },

    'paymentmethod': {
        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'data_source': 'Veri Kaynağı',
        'standard_reference': 'Standart Referans Kodu'

    },

    'paymenttype': {
        'code': 'Kodu',
        'name': 'Adı',
        'description': 'Açıklama',
        'data_source': 'Veri Kaynağı',
        'name_en': 'Adı(EN)'
    },
    'customstype': {
        'code': 'Kodu',
        'name': 'Adı',
        'description': 'Açıklama',
        'data_source': 'Veri Kaynağı'

    },
    'chiefcustomsoffice': {
        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    },

    'customsoffice': {
        'code': 'Gümrük Kodu',
        'name': 'Gümrük Adı',
        'customs_type': 'Gümrük Tipi',
        'chief_customs': 'Üst Müdürlük Kodu',
        'city': 'Şehir',
        'data_source': 'Veri Kaynağı'
    },
    'port': {

        'code': 'Kodu',
        'name': 'Adı',
        'country': 'Ülke',
        'city': 'Şehir',
        'data_source': 'Veri Kaynağı'
    },
    'requireddocument': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'edi_code': "Edi Kodu",
        'data_source': 'Veri Kaynağı'
    },
    'deliverymethod': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'data_source': 'Veri Kaynağı'

    },
    'airport': {
        'code_iata': 'IATA Kodu',
        'code_icao': 'ICAO Kodu',
        'city': 'Yerleşim',
        'country': 'Ülke',
        'name': 'Adı',
        'latitude_degree': 'Enlem',
        'longitude_degree': 'Boylam',
        'data_source': 'Veri kaynağı'
    },
    'taxcode': {

        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    },

    'transporttype': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'transport_type': 'Standart Referansı',
        'data_source': 'Veri Kaynağı'

    },
    'containercode': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'data_source': 'Veri Kaynağı'
    },
    'quantitytype': {

        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'unit_symbol': "Sembol",
        'data_source': 'Veri Kaynağı'
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
        'data_source': 'Veri Kaynağı'
    },
    'bankbranches': {

        'bank': 'Banka',
        'name': 'Şube Adı',
        'branches_code': 'Şube Kodu',
        'city': 'Şehir',
        'data_source': 'Veri Kaynağı'
    },
    'datasource': {

        'name': 'Adı',
        'source_type': 'Tipi',
        'description': 'Açıklama',
        'origin_country': 'Yayımlayan Ülke'
    },
    'transportvehicle': {

        'data_source': 'Veri Kaynağı',
        'code': 'Kodu',
        'name': 'Adı',
        'name_en': 'Adı(EN)',
        'description': 'Açıklama'
    },
    'gtipcode': {
        'data_source': 'Veri Kaynağı',
        'code': 'Kodu',
        'desc': 'Açıklama'

    },
    "transactiontype": {

        'code': 'Kodu',
        'name': ' Adı',
        'data_source': 'Veri Kaynağı'
    },
    'additionalinfocode': {
        'code': 'Kodu',
        'description': 'Açıklama',
        'value': 'Değeri',
        'data_source': 'Veri Kaynağı'
    },
    'antidumpingcompany': {
        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    },
    'internationalagreement': {
        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    },
    'simplifiedprocedure': {
        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    },
    'exemptioncode': {
        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    },
    'regimecode': {
        'code': 'Kodu',
        'name': 'Adı',
        'data_source': 'Veri Kaynağı'

    }

}

# constants.py
FK_M2M_REPRESENTATIVE_FIELDS = {
    "Country": "country_name_tr",
    "City": "name",
    "CurrencyType": "name_tr",
    "ChiefCustomsOffice": "code",
    "CustomsType": "code",
    "Bank": 'bank_name',
    "DataSource": 'name',
    'PaymentMethod': 'code',
    'TransportType': 'code'
}

SYSTEM_FIELDS = [
    "record_uuid", "created_by", "updated_by",
    "custom_model", "created_at", "updated_at"

]


# constants.py

ROLE_ADMIN = "admin"
ROLE_MUSAVIR = "consultant"
ROLE_MUSTERI = "client"

# Roller bazında erişim kısıtlaması: app bazlı
ROLE_APP_BLACKLIST = {
    ROLE_MUSTERI: ["customs_general"],  # müşteri genel tanımlamaları görmesin
    ROLE_MUSAVIR: ["products"],         # müşavir ürünlerle ilgilenmesin
    # admin her şeye erişebilir
}