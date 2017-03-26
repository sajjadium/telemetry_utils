import hashlib
import struct

ERRORS = {
    0: "SUCCESS",
    1: "SSL_ERROR_US_ONLY_SERVER",
    2: "SSL_ERROR_NO_CYPHER_OVERLAP",
    3: "SSL_ERROR_NO_CERTIFICATE",
    4: "SSL_ERROR_BAD_CERTIFICATE",
    5: "SSL_ERROR_UNUSED_5",
    6: "SSL_ERROR_BAD_CLIENT",
    7: "SSL_ERROR_BAD_SERVER",
    8: "SSL_ERROR_UNSUPPORTED_CERTIFICATE_TYPE",
    9: "SSL_ERROR_UNSUPPORTED_VERSION",
    10: "SSL_ERROR_UNUSED_10",
    11: "SSL_ERROR_WRONG_CERTIFICATE",
    12: "SSL_ERROR_BAD_CERT_DOMAIN",
    13: "SSL_ERROR_POST_WARNING",
    14: "SSL_ERROR_SSL2_DISABLED",
    15: "SSL_ERROR_BAD_MAC_READ",
    16: "SSL_ERROR_BAD_MAC_ALERT",
    17: "SSL_ERROR_BAD_CERT_ALERT",
    18: "SSL_ERROR_REVOKED_CERT_ALERT",
    19: "SSL_ERROR_EXPIRED_CERT_ALERT",
    20: "SSL_ERROR_SSL_DISABLED",
    21: "SSL_ERROR_FORTEZZA_PQG",
    22: "SSL_ERROR_UNKNOWN_CIPHER_SUITE",
    23: "SSL_ERROR_NO_CIPHERS_SUPPORTED",
    24: "SSL_ERROR_BAD_BLOCK_PADDING",
    25: "SSL_ERROR_RX_RECORD_TOO_LONG",
    26: "SSL_ERROR_TX_RECORD_TOO_LONG",
    27: "SSL_ERROR_RX_MALFORMED_HELLO_REQUEST",
    28: "SSL_ERROR_RX_MALFORMED_CLIENT_HELLO",
    29: "SSL_ERROR_RX_MALFORMED_SERVER_HELLO",
    30: "SSL_ERROR_RX_MALFORMED_CERTIFICATE",
    31: "SSL_ERROR_RX_MALFORMED_SERVER_KEY_EXCH",
    32: "SSL_ERROR_RX_MALFORMED_CERT_REQUEST",
    33: "SSL_ERROR_RX_MALFORMED_HELLO_DONE",
    34: "SSL_ERROR_RX_MALFORMED_CERT_VERIFY",
    35: "SSL_ERROR_RX_MALFORMED_CLIENT_KEY_EXCH",
    36: "SSL_ERROR_RX_MALFORMED_FINISHED",
    37: "SSL_ERROR_RX_MALFORMED_CHANGE_CIPHER",
    38: "SSL_ERROR_RX_MALFORMED_ALERT",
    39: "SSL_ERROR_RX_MALFORMED_HANDSHAKE",
    40: "SSL_ERROR_RX_MALFORMED_APPLICATION_DATA",
    41: "SSL_ERROR_RX_UNEXPECTED_HELLO_REQUEST",
    42: "SSL_ERROR_RX_UNEXPECTED_CLIENT_HELLO",
    43: "SSL_ERROR_RX_UNEXPECTED_SERVER_HELLO",
    44: "SSL_ERROR_RX_UNEXPECTED_CERTIFICATE",
    45: "SSL_ERROR_RX_UNEXPECTED_SERVER_KEY_EXCH",
    46: "SSL_ERROR_RX_UNEXPECTED_CERT_REQUEST",
    47: "SSL_ERROR_RX_UNEXPECTED_HELLO_DONE",
    48: "SSL_ERROR_RX_UNEXPECTED_CERT_VERIFY",
    49: "SSL_ERROR_RX_UNEXPECTED_CLIENT_KEY_EXCH",
    50: "SSL_ERROR_RX_UNEXPECTED_FINISHED",
    51: "SSL_ERROR_RX_UNEXPECTED_CHANGE_CIPHER",
    52: "SSL_ERROR_RX_UNEXPECTED_ALERT",
    53: "SSL_ERROR_RX_UNEXPECTED_HANDSHAKE",
    54: "SSL_ERROR_RX_UNEXPECTED_APPLICATION_DATA",
    55: "SSL_ERROR_RX_UNKNOWN_RECORD_TYPE",
    56: "SSL_ERROR_RX_UNKNOWN_HANDSHAKE",
    57: "SSL_ERROR_RX_UNKNOWN_ALERT",
    58: "SSL_ERROR_CLOSE_NOTIFY_ALERT",
    59: "SSL_ERROR_HANDSHAKE_UNEXPECTED_ALERT",
    60: "SSL_ERROR_DECOMPRESSION_FAILURE_ALERT",
    61: "SSL_ERROR_HANDSHAKE_FAILURE_ALERT",
    62: "SSL_ERROR_ILLEGAL_PARAMETER_ALERT",
    63: "SSL_ERROR_UNSUPPORTED_CERT_ALERT",
    64: "SSL_ERROR_CERTIFICATE_UNKNOWN_ALERT",
    65: "SSL_ERROR_GENERATE_RANDOM_FAILURE",
    66: "SSL_ERROR_SIGN_HASHES_FAILURE",
    67: "SSL_ERROR_EXTRACT_PUBLIC_KEY_FAILURE",
    68: "SSL_ERROR_SERVER_KEY_EXCHANGE_FAILURE",
    69: "SSL_ERROR_CLIENT_KEY_EXCHANGE_FAILURE",
    70: "SSL_ERROR_ENCRYPTION_FAILURE",
    71: "SSL_ERROR_DECRYPTION_FAILURE",
    72: "SSL_ERROR_SOCKET_WRITE_FAILURE",
    73: "SSL_ERROR_MD5_DIGEST_FAILURE",
    74: "SSL_ERROR_SHA_DIGEST_FAILURE",
    75: "SSL_ERROR_MAC_COMPUTATION_FAILURE",
    76: "SSL_ERROR_SYM_KEY_CONTEXT_FAILURE",
    77: "SSL_ERROR_SYM_KEY_UNWRAP_FAILURE",
    78: "SSL_ERROR_PUB_KEY_SIZE_LIMIT_EXCEEDED",
    79: "SSL_ERROR_IV_PARAM_FAILURE",
    80: "SSL_ERROR_INIT_CIPHER_SUITE_FAILURE",
    81: "SSL_ERROR_SESSION_KEY_GEN_FAILURE",
    82: "SSL_ERROR_NO_SERVER_KEY_FOR_ALG",
    83: "SSL_ERROR_TOKEN_INSERTION_REMOVAL",
    84: "SSL_ERROR_TOKEN_SLOT_NOT_FOUND",
    85: "SSL_ERROR_NO_COMPRESSION_OVERLAP",
    86: "SSL_ERROR_HANDSHAKE_NOT_COMPLETED",
    87: "SSL_ERROR_BAD_HANDSHAKE_HASH_VALUE",
    88: "SSL_ERROR_CERT_KEA_MISMATCH",
    89: "SSL_ERROR_NO_TRUSTED_SSL_CLIENT_CA",
    90: "SSL_ERROR_SESSION_NOT_FOUND",
    91: "SSL_ERROR_DECRYPTION_FAILED_ALERT",
    92: "SSL_ERROR_RECORD_OVERFLOW_ALERT",
    93: "SSL_ERROR_UNKNOWN_CA_ALERT",
    94: "SSL_ERROR_ACCESS_DENIED_ALERT",
    95: "SSL_ERROR_DECODE_ERROR_ALERT",
    96: "SSL_ERROR_DECRYPT_ERROR_ALERT",
    97: "SSL_ERROR_EXPORT_RESTRICTION_ALERT",
    98: "SSL_ERROR_PROTOCOL_VERSION_ALERT",
    99: "SSL_ERROR_INSUFFICIENT_SECURITY_ALERT",
    100: "SSL_ERROR_INTERNAL_ERROR_ALERT",
    101: "SSL_ERROR_USER_CANCELED_ALERT",
    102: "SSL_ERROR_NO_RENEGOTIATION_ALERT",
    103: "SSL_ERROR_SERVER_CACHE_NOT_CONFIGURED",
    104: "SSL_ERROR_UNSUPPORTED_EXTENSION_ALERT",
    105: "SSL_ERROR_CERTIFICATE_UNOBTAINABLE_ALERT",
    106: "SSL_ERROR_UNRECOGNIZED_NAME_ALERT",
    107: "SSL_ERROR_BAD_CERT_STATUS_RESPONSE_ALERT",
    108: "SSL_ERROR_BAD_CERT_HASH_VALUE_ALERT",
    109: "SSL_ERROR_RX_UNEXPECTED_NEW_SESSION_TICKET",
    110: "SSL_ERROR_RX_MALFORMED_NEW_SESSION_TICKET",
    111: "SSL_ERROR_DECOMPRESSION_FAILURE",
    112: "SSL_ERROR_RENEGOTIATION_NOT_ALLOWED",
    113: "SSL_ERROR_UNSAFE_NEGOTIATION",
    114: "SSL_ERROR_RX_UNEXPECTED_UNCOMPRESSED_RECORD",
    115: "SSL_ERROR_WEAK_SERVER_EPHEMERAL_DH_KEY",
    116: "SSL_ERROR_NEXT_PROTOCOL_DATA_INVALID",
    117: "SSL_ERROR_FEATURE_NOT_SUPPORTED_FOR_SSL2",
    118: "SSL_ERROR_FEATURE_NOT_SUPPORTED_FOR_SERVERS",
    119: "SSL_ERROR_FEATURE_NOT_SUPPORTED_FOR_CLIENTS",
    120: "SSL_ERROR_INVALID_VERSION_RANGE",
    121: "SSL_ERROR_CIPHER_DISALLOWED_FOR_VERSION",
    122: "SSL_ERROR_RX_MALFORMED_HELLO_VERIFY_REQUEST",
    123: "SSL_ERROR_RX_UNEXPECTED_HELLO_VERIFY_REQUEST",
    124: "SSL_ERROR_FEATURE_NOT_SUPPORTED_FOR_VERSION",
    125: "SSL_ERROR_RX_UNEXPECTED_CERT_STATUS",
    126: "SSL_ERROR_UNSUPPORTED_HASH_ALGORITHM",
    127: "SSL_ERROR_DIGEST_FAILURE",
    128: "SSL_ERROR_INCORRECT_SIGNATURE_ALGORITHM",
    129: "SSL_ERROR_NEXT_PROTOCOL_NO_CALLBACK",
    130: "SSL_ERROR_NEXT_PROTOCOL_NO_PROTOCOL",
    131: "SSL_ERROR_INAPPROPRIATE_FALLBACK_ALERT",
    132: "SSL_ERROR_WEAK_SERVER_CERT_KEY",
    133: "SSL_ERROR_RX_SHORT_DTLS_READ",
    134: "SSL_ERROR_NO_SUPPORTED_SIGNATURE_ALGORITHM",
    135: "SSL_ERROR_UNSUPPORTED_SIGNATURE_ALGORITHM",
    136: "SSL_ERROR_MISSING_EXTENDED_MASTER_SECRET",
    137: "SSL_ERROR_UNEXPECTED_EXTENDED_MASTER_SECRET",
    138: "SSL_ERROR_RX_MALFORMED_KEY_SHARE",
    139: "SSL_ERROR_MISSING_KEY_SHARE",
    140: "SSL_ERROR_RX_MALFORMED_ECDHE_KEY_SHARE",
    141: "SSL_ERROR_RX_MALFORMED_DHE_KEY_SHARE",
    142: "SSL_ERROR_RX_UNEXPECTED_ENCRYPTED_EXTENSIONS",
    143: "SSL_ERROR_MISSING_EXTENSION_ALERT",
    144: "SSL_ERROR_KEY_EXCHANGE_FAILURE",
    145: "SSL_ERROR_EXTENSION_DISALLOWED_FOR_VERSION",
    146: "SSL_ERROR_RX_MALFORMED_ENCRYPTED_EXTENSIONS",
    147: "SSL_ERROR_MALFORMED_PRE_SHARED_KEY",
    148: "SSL_ERROR_MALFORMED_EARLY_DATA",
    149: "SSL_ERROR_END_OF_EARLY_DATA_ALERT",
    150: "SSL_ERROR_MISSING_ALPN_EXTENSION",
    151: "SSL_ERROR_RX_UNEXPECTED_EXTENSION",
    152: "SSL_ERROR_MISSING_SUPPORTED_GROUPS_EXTENSION",
    153: "SSL_ERROR_TOO_MANY_RECORDS",
    154: "SSL_ERROR_RX_UNEXPECTED_HELLO_RETRY_REQUEST",
    155: "SSL_ERROR_RX_MALFORMED_HELLO_RETRY_REQUEST",
    156: "SSL_ERROR_BAD_2ND_CLIENT_HELLO",
    157: "SSL_ERROR_MISSING_SIGNATURE_ALGORITHMS_EXTENSION",
    158: "SSL_ERROR_MALFORMED_PSK_KEY_EXCHANGE_MODES",
    159: "SSL_ERROR_MISSING_PSK_KEY_EXCHANGE_MODES",
    160: "SSL_ERROR_DOWNGRADE_WITH_EARLY_DATA",
    256: "SEC_ERROR_IO",
    257: "SEC_ERROR_LIBRARY_FAILURE",
    258: "SEC_ERROR_BAD_DATA",
    259: "SEC_ERROR_OUTPUT_LEN",
    260: "SEC_ERROR_INPUT_LEN",
    261: "SEC_ERROR_INVALID_ARGS",
    262: "SEC_ERROR_INVALID_ALGORITHM",
    263: "SEC_ERROR_INVALID_AVA",
    264: "SEC_ERROR_INVALID_TIME",
    265: "SEC_ERROR_BAD_DER",
    266: "SEC_ERROR_BAD_SIGNATURE",
    267: "SEC_ERROR_EXPIRED_CERTIFICATE",
    268: "SEC_ERROR_REVOKED_CERTIFICATE",
    269: "SEC_ERROR_UNKNOWN_ISSUER",
    270: "SEC_ERROR_BAD_KEY",
    271: "SEC_ERROR_BAD_PASSWORD",
    272: "SEC_ERROR_RETRY_PASSWORD",
    273: "SEC_ERROR_NO_NODELOCK",
    274: "SEC_ERROR_BAD_DATABASE",
    275: "SEC_ERROR_NO_MEMORY",
    276: "SEC_ERROR_UNTRUSTED_ISSUER",
    277: "SEC_ERROR_UNTRUSTED_CERT",
    278: "SEC_ERROR_DUPLICATE_CERT",
    279: "SEC_ERROR_DUPLICATE_CERT_NAME",
    280: "SEC_ERROR_ADDING_CERT",
    281: "SEC_ERROR_FILING_KEY",
    282: "SEC_ERROR_NO_KEY",
    283: "SEC_ERROR_CERT_VALID",
    284: "SEC_ERROR_CERT_NOT_VALID",
    285: "SEC_ERROR_CERT_NO_RESPONSE",
    286: "SEC_ERROR_EXPIRED_ISSUER_CERTIFICATE",
    287: "SEC_ERROR_CRL_EXPIRED",
    288: "SEC_ERROR_CRL_BAD_SIGNATURE",
    289: "SEC_ERROR_CRL_INVALID",
    290: "SEC_ERROR_EXTENSION_VALUE_INVALID",
    291: "SEC_ERROR_EXTENSION_NOT_FOUND",
    292: "SEC_ERROR_CA_CERT_INVALID",
    293: "SEC_ERROR_PATH_LEN_CONSTRAINT_INVALID",
    294: "SEC_ERROR_CERT_USAGES_INVALID",
    295: "SEC_INTERNAL_ONLY",
    296: "SEC_ERROR_INVALID_KEY",
    297: "SEC_ERROR_UNKNOWN_CRITICAL_EXTENSION",
    298: "SEC_ERROR_OLD_CRL",
    299: "SEC_ERROR_NO_EMAIL_CERT",
    300: "SEC_ERROR_NO_RECIPIENT_CERTS_QUERY",
    301: "SEC_ERROR_NOT_A_RECIPIENT",
    302: "SEC_ERROR_PKCS7_KEYALG_MISMATCH",
    303: "SEC_ERROR_PKCS7_BAD_SIGNATURE",
    304: "SEC_ERROR_UNSUPPORTED_KEYALG",
    305: "SEC_ERROR_DECRYPTION_DISALLOWED",
    306: "SEC_FORTEZZA_BAD_CARD",
    307: "SEC_FORTEZZA_NO_CARD",
    308: "SEC_FORTEZZA_NONE_SELECTED",
    309: "SEC_FORTEZZA_MORE_INFO",
    310: "SEC_FORTEZZA_PERSON_NOT_FOUND",
    311: "SEC_FORTEZZA_NO_MORE_INFO",
    312: "SEC_FORTEZZA_BAD_PIN",
    313: "SEC_FORTEZZA_PERSON_ERROR",
    314: "SEC_ERROR_NO_KRL",
    315: "SEC_ERROR_KRL_EXPIRED",
    316: "SEC_ERROR_KRL_BAD_SIGNATURE",
    317: "SEC_ERROR_REVOKED_KEY",
    318: "SEC_ERROR_KRL_INVALID",
    319: "SEC_ERROR_NEED_RANDOM",
    320: "SEC_ERROR_NO_MODULE",
    321: "SEC_ERROR_NO_TOKEN",
    322: "SEC_ERROR_READ_ONLY",
    323: "SEC_ERROR_NO_SLOT_SELECTED",
    324: "SEC_ERROR_CERT_NICKNAME_COLLISION",
    325: "SEC_ERROR_KEY_NICKNAME_COLLISION",
    326: "SEC_ERROR_SAFE_NOT_CREATED",
    327: "SEC_ERROR_BAGGAGE_NOT_CREATED",
    331: "SEC_ERROR_BAD_EXPORT_ALGORITHM",
    332: "SEC_ERROR_EXPORTING_CERTIFICATES",
    333: "SEC_ERROR_IMPORTING_CERTIFICATES",
    334: "SEC_ERROR_PKCS12_DECODING_PFX",
    335: "SEC_ERROR_PKCS12_INVALID_MAC",
    336: "SEC_ERROR_PKCS12_UNSUPPORTED_MAC_ALGORITHM",
    337: "SEC_ERROR_PKCS12_UNSUPPORTED_TRANSPORT_MODE",
    338: "SEC_ERROR_PKCS12_CORRUPT_PFX_STRUCTURE",
    339: "SEC_ERROR_PKCS12_UNSUPPORTED_PBE_ALGORITHM",
    340: "SEC_ERROR_PKCS12_UNSUPPORTED_VERSION",
    341: "SEC_ERROR_PKCS12_PRIVACY_PASSWORD_INCORRECT",
    342: "SEC_ERROR_PKCS12_CERT_COLLISION",
    343: "SEC_ERROR_USER_CANCELLED",
    344: "SEC_ERROR_PKCS12_DUPLICATE_DATA",
    345: "SEC_ERROR_MESSAGE_SEND_ABORTED",
    346: "SEC_ERROR_INADEQUATE_KEY_USAGE",
    347: "SEC_ERROR_INADEQUATE_CERT_TYPE",
    348: "SEC_ERROR_CERT_ADDR_MISMATCH",
    349: "SEC_ERROR_PKCS12_UNABLE_TO_IMPORT_KEY",
    350: "SEC_ERROR_PKCS12_IMPORTING_CERT_CHAIN",
    351: "SEC_ERROR_PKCS12_UNABLE_TO_LOCATE_OBJECT_BY_NAME",
    352: "SEC_ERROR_PKCS12_UNABLE_TO_EXPORT_KEY",
    353: "SEC_ERROR_PKCS12_UNABLE_TO_WRITE",
    354: "SEC_ERROR_PKCS12_UNABLE_TO_READ",
    355: "SEC_ERROR_PKCS12_KEY_DATABASE_NOT_INITIALIZED",
    356: "SEC_ERROR_KEYGEN_FAIL",
    357: "SEC_ERROR_INVALID_PASSWORD",
    358: "SEC_ERROR_RETRY_OLD_PASSWORD",
    359: "SEC_ERROR_BAD_NICKNAME",
    360: "SEC_ERROR_NOT_FORTEZZA_ISSUER",
    361: "SEC_ERROR_CANNOT_MOVE_SENSITIVE_KEY",
    362: "SEC_ERROR_JS_INVALID_MODULE_NAME",
    363: "SEC_ERROR_JS_INVALID_DLL",
    364: "SEC_ERROR_JS_ADD_MOD_FAILURE",
    365: "SEC_ERROR_JS_DEL_MOD_FAILURE",
    366: "SEC_ERROR_OLD_KRL",
    367: "SEC_ERROR_CKL_CONFLICT",
    368: "SEC_ERROR_CERT_NOT_IN_NAME_SPACE",
    369: "SEC_ERROR_KRL_NOT_YET_VALID",
    370: "SEC_ERROR_CRL_NOT_YET_VALID",
    371: "SEC_ERROR_UNKNOWN_CERT",
    372: "SEC_ERROR_UNKNOWN_SIGNER",
    373: "SEC_ERROR_CERT_BAD_ACCESS_LOCATION",
    374: "SEC_ERROR_OCSP_UNKNOWN_RESPONSE_TYPE",
    375: "SEC_ERROR_OCSP_BAD_HTTP_RESPONSE",
    376: "SEC_ERROR_OCSP_MALFORMED_REQUEST",
    377: "SEC_ERROR_OCSP_SERVER_ERROR",
    378: "SEC_ERROR_OCSP_TRY_SERVER_LATER",
    379: "SEC_ERROR_OCSP_REQUEST_NEEDS_SIG",
    380: "SEC_ERROR_OCSP_UNAUTHORIZED_REQUEST",
    381: "SEC_ERROR_OCSP_UNKNOWN_RESPONSE_STATUS",
    382: "SEC_ERROR_OCSP_UNKNOWN_CERT",
    383: "SEC_ERROR_OCSP_NOT_ENABLED",
    384: "SEC_ERROR_OCSP_NO_DEFAULT_RESPONDER",
    385: "SEC_ERROR_OCSP_MALFORMED_RESPONSE",
    386: "SEC_ERROR_OCSP_UNAUTHORIZED_RESPONSE",
    387: "SEC_ERROR_OCSP_FUTURE_RESPONSE",
    388: "SEC_ERROR_OCSP_OLD_RESPONSE",
    389: "SEC_ERROR_DIGEST_NOT_FOUND",
    390: "SEC_ERROR_UNSUPPORTED_MESSAGE_TYPE",
    391: "SEC_ERROR_MODULE_STUCK",
    392: "SEC_ERROR_BAD_TEMPLATE",
    393: "SEC_ERROR_CRL_NOT_FOUND",
    394: "SEC_ERROR_REUSED_ISSUER_AND_SERIAL",
    395: "SEC_ERROR_BUSY",
    396: "SEC_ERROR_EXTRA_INPUT",
    397: "SEC_ERROR_UNSUPPORTED_ELLIPTIC_CURVE",
    398: "SEC_ERROR_UNSUPPORTED_EC_POINT_FORM",
    399: "SEC_ERROR_UNRECOGNIZED_OID",
    400: "SEC_ERROR_OCSP_INVALID_SIGNING_CERT",
    401: "SEC_ERROR_REVOKED_CERTIFICATE_CRL",
    402: "SEC_ERROR_REVOKED_CERTIFICATE_OCSP",
    403: "SEC_ERROR_CRL_INVALID_VERSION",
    404: "SEC_ERROR_CRL_V1_CRITICAL_EXTENSION",
    405: "SEC_ERROR_CRL_UNKNOWN_CRITICAL_EXTENSION",
    406: "SEC_ERROR_UNKNOWN_OBJECT_TYPE",
    407: "SEC_ERROR_INCOMPATIBLE_PKCS11",
    408: "SEC_ERROR_NO_EVENT",
    409: "SEC_ERROR_CRL_ALREADY_EXISTS",
    410: "SEC_ERROR_NOT_INITIALIZED",
    411: "SEC_ERROR_TOKEN_NOT_LOGGED_IN",
    412: "SEC_ERROR_OCSP_RESPONDER_CERT_INVALID",
    413: "SEC_ERROR_OCSP_BAD_SIGNATURE",
    414: "SEC_ERROR_OUT_OF_SEARCH_LIMITS",
    415: "SEC_ERROR_INVALID_POLICY_MAPPING",
    416: "SEC_ERROR_POLICY_VALIDATION_FAILED",
    417: "SEC_ERROR_UNKNOWN_AIA_LOCATION_TYPE",
    418: "SEC_ERROR_BAD_HTTP_RESPONSE",
    419: "SEC_ERROR_BAD_LDAP_RESPONSE",
    420: "SEC_ERROR_FAILED_TO_ENCODE_DATA",
    421: "SEC_ERROR_BAD_INFO_ACCESS_LOCATION",
    422: "SEC_ERROR_LIBPKIX_INTERNAL",
    423: "SEC_ERROR_PKCS11_GENERAL_ERROR",
    424: "SEC_ERROR_PKCS11_FUNCTION_FAILED",
    425: "SEC_ERROR_PKCS11_DEVICE_ERROR",
    426: "SEC_ERROR_BAD_INFO_ACCESS_METHOD",
    427: "SEC_ERROR_CRL_IMPORT_FAILED",
    428: "SEC_ERROR_EXPIRED_PASSWORD",
    429: "SEC_ERROR_LOCKED_PASSWORD",
    430: "SEC_ERROR_UNKNOWN_PKCS11_ERROR",
    431: "SEC_ERROR_BAD_CRL_DP_URL",
    432: "SEC_ERROR_CERT_SIGNATURE_ALGORITHM_DISABLED",
    433: "SEC_ERROR_LEGACY_DATABASE",
    434: "SEC_ERROR_APPLICATION_CALLBACK_ERROR",
    512: "PR_OUT_OF_MEMORY_ERROR",
    513: "PR_BAD_DESCRIPTOR_ERROR",
    514: "PR_WOULD_BLOCK_ERROR",
    515: "PR_ACCESS_FAULT_ERROR",
    516: "PR_INVALID_METHOD_ERROR",
    517: "PR_ILLEGAL_ACCESS_ERROR",
    518: "PR_UNKNOWN_ERROR",
    519: "PR_PENDING_INTERRUPT_ERROR",
    520: "PR_NOT_IMPLEMENTED_ERROR",
    521: "PR_IO_ERROR",
    522: "PR_IO_TIMEOUT_ERROR",
    523: "PR_IO_PENDING_ERROR",
    524: "PR_DIRECTORY_OPEN_ERROR",
    525: "PR_INVALID_ARGUMENT_ERROR",
    526: "PR_ADDRESS_NOT_AVAILABLE_ERROR",
    527: "PR_ADDRESS_NOT_SUPPORTED_ERROR",
    528: "PR_IS_CONNECTED_ERROR",
    529: "PR_BAD_ADDRESS_ERROR",
    530: "PR_ADDRESS_IN_USE_ERROR",
    531: "PR_CONNECT_REFUSED_ERROR",
    532: "PR_NETWORK_UNREACHABLE_ERROR",
    533: "PR_CONNECT_TIMEOUT_ERROR",
    534: "PR_NOT_CONNECTED_ERROR",
    535: "PR_LOAD_LIBRARY_ERROR",
    536: "PR_UNLOAD_LIBRARY_ERROR",
    537: "PR_FIND_SYMBOL_ERROR",
    538: "PR_INSUFFICIENT_RESOURCES_ERROR",
    539: "PR_DIRECTORY_LOOKUP_ERROR",
    540: "PR_TPD_RANGE_ERROR",
    541: "PR_PROC_DESC_TABLE_FULL_ERROR",
    542: "PR_SYS_DESC_TABLE_FULL_ERROR",
    543: "PR_NOT_SOCKET_ERROR",
    544: "PR_NOT_TCP_SOCKET_ERROR",
    545: "PR_SOCKET_ADDRESS_IS_BOUND_ERROR",
    546: "PR_NO_ACCESS_RIGHTS_ERROR",
    547: "PR_OPERATION_NOT_SUPPORTED_ERROR",
    548: "PR_PROTOCOL_NOT_SUPPORTED_ERROR",
    549: "PR_REMOTE_FILE_ERROR",
    550: "PR_BUFFER_OVERFLOW_ERROR",
    551: "PR_CONNECT_RESET_ERROR",
    552: "PR_RANGE_ERROR",
    553: "PR_DEADLOCK_ERROR",
    554: "PR_FILE_IS_LOCKED_ERROR",
    555: "PR_FILE_TOO_BIG_ERROR",
    556: "PR_NO_DEVICE_SPACE_ERROR",
    557: "PR_PIPE_ERROR",
    558: "PR_NO_SEEK_DEVICE_ERROR",
    559: "PR_IS_DIRECTORY_ERROR",
    560: "PR_LOOP_ERROR",
    561: "PR_NAME_TOO_LONG_ERROR",
    562: "PR_FILE_NOT_FOUND_ERROR",
    563: "PR_NOT_DIRECTORY_ERROR",
    564: "PR_READ_ONLY_FILESYSTEM_ERROR",
    565: "PR_DIRECTORY_NOT_EMPTY_ERROR",
    566: "PR_FILESYSTEM_MOUNTED_ERROR",
    567: "PR_NOT_SAME_DEVICE_ERROR",
    568: "PR_DIRECTORY_CORRUPTED_ERROR",
    569: "PR_FILE_EXISTS_ERROR",
    570: "PR_MAX_DIRECTORY_ENTRIES_ERROR",
    571: "PR_INVALID_DEVICE_STATE_ERROR",
    572: "PR_DEVICE_IS_LOCKED_ERROR",
    573: "PR_NO_MORE_FILES_ERROR",
    574: "PR_END_OF_FILE_ERROR",
    575: "PR_FILE_SEEK_ERROR",
    576: "PR_FILE_IS_BUSY_ERROR",
    577: "PR_OPERATION_ABORTED_ERROR",
    578: "PR_IN_PROGRESS_ERROR",
    579: "PR_ALREADY_INITIATED_ERROR",
    580: "PR_GROUP_EMPTY_ERROR",
    581: "PR_INVALID_STATE_ERROR",
    582: "PR_NETWORK_DOWN_ERROR",
    583: "PR_SOCKET_SHUTDOWN_ERROR",
    584: "PR_CONNECT_ABORTED_ERROR",
    585: "PR_HOST_UNREACHABLE_ERROR",
    586: "PR_LIBRARY_NOT_LOADED_ERROR",
    587: "PR_CALL_ONCE_ERROR",
    588: "PR_MAX_ERROR",
    640: "MOZILLA_PKIX_ERROR_KEY_PINNING_FAILURE",
    641: "MOZILLA_PKIX_ERROR_CA_CERT_USED_AS_END_ENTITY",
    642: "MOZILLA_PKIX_ERROR_INADEQUATE_KEY_SIZE",
    643: "MOZILLA_PKIX_ERROR_V1_CERT_USED_AS_CA",
    644: "MOZILLA_PKIX_ERROR_NO_RFC822NAME_MATCH",
    645: "MOZILLA_PKIX_ERROR_NOT_YET_VALID_CERTIFICATE",
    646: "MOZILLA_PKIX_ERROR_NOT_YET_VALID_ISSUER_CERTIFICATE",
    647: "MOZILLA_PKIX_ERROR_SIGNATURE_ALGORITHM_MISMATCH",
    648: "MOZILLA_PKIX_ERROR_OCSP_RESPONSE_FOR_CERT_MISSING",
    649: "MOZILLA_PKIX_ERROR_VALIDITY_TOO_LONG",
    650: "MOZILLA_PKIX_ERROR_REQUIRED_TLS_FEATURE_MISSING",
    651: "MOZILLA_PKIX_ERROR_INVALID_INTEGER_ENCODING",
    652: "MOZILLA_PKIX_ERROR_EMPTY_ISSUER_NAME",
    671: "UNKNOWN_ERROR",
}
   
def categorize(e):
    RETRY_RESULTS = [
        "SSL_ERROR_BAD_MAC_ALERT",
        "SSL_ERROR_BAD_MAC_READ",
        "SSL_ERROR_HANDSHAKE_FAILURE_ALERT",
        "SSL_ERROR_HANDSHAKE_UNEXPECTED_ALERT",
        "SSL_ERROR_ILLEGAL_PARAMETER_ALERT",
        "SSL_ERROR_NO_CYPHER_OVERLAP",
        "SSL_ERROR_UNSUPPORTED_VERSION",
        "SSL_ERROR_PROTOCOL_VERSION_ALERT",
        "SSL_ERROR_BAD_HANDSHAKE_HASH_VALUE",
        "SSL_ERROR_DECODE_ERROR_ALERT",
        "PR_CONNECT_RESET_ERROR",
        "PR_END_OF_FILE_ERROR",
        "SSL_ERROR_INTERNAL_ERROR_ALERT",
    ]

    FAIL_RESULTS = [
        "SSL_ERROR_BAD_CERT_DOMAIN",
        "SEC_ERROR_EXPIRED_CERTIFICATE",
        "SEC_ERROR_UNKNOWN_ISSUER",
        "SEC_ERROR_CERT_SIGNATURE_ALGORITHM_DISABLED",
        "SSL_ERROR_UNRECOGNIZED_NAME_ALERT",
    ]

    if e == "SUCCESS":
        return e
    if e in RETRY_RESULTS:
        return "RETRY"
    if e in FAIL_RESULTS:
        return "FAIL"
    return "UNKNOWN"

def translate_errors(errors):
    COUNTS = {}
    RESULTS= []
    SUM = 0
    CATEGORIES = {
        "SUCCESS":0,
        "FAIL":0,
        "RETRY":0,
        "UNKNOWN":0,
    }
    
    for err in errors:
        RESULTS.append(ERRORS[err])
        COUNTS[ERRORS[err]] = errors[err]
        CATEGORIES[categorize(ERRORS[err])] += errors[err]
        SUM += errors[err]

    RESULTS.sort(lambda a,b: cmp(COUNTS[a], COUNTS[b]))
    for r in RESULTS:
        print r,COUNTS[r],float(COUNTS[r])/float(SUM),categorize(r)
            
    print    
    for c in CATEGORIES:
        print c, CATEGORIES[c],float(CATEGORIES[c])/float(SUM)    

    print
    print "TOTAL", SUM


def predict_arm(x):
    h = hashlib.sha256(x["clientId"] + "tls13-comparison-all-v1@mozilla.org")
    variate = (struct.unpack(">L", h.digest()[0:4])[0]) / 0xffffffff
    if variate < 0.5:
        return "treatment"
    else:
        return "control"

HTTP_DISPOSITION_CODES = {
    0:"HTTP:Cancel", 1:"HTTP:Disk", 2:"HTTP:NetOK", 3:"HTTP:NetEarlyFail", 4:"HTTP:NetlateFail",
    8:"HTTPS:Cancel", 9:"HTTPS:Disk", 10:"HTTPS:NetOK", 11:"HTTPS:NetEarlyFail", 12:"HTTPS:NetlateFail"
}
    
def translate_histogram(hist, table):
    COUNTS = {}
    RESULTS= []
    SUM = 0
    for err in hist:
        string = "CODE_%d"%err
        if err in table:
            string = table[err]
        RESULTS.append(string)
        COUNTS[string] = hist[err]
        SUM += hist[err]
    RESULTS.sort(lambda a,b: cmp(COUNTS[a], COUNTS[b]))
    for r in RESULTS:
        print r,COUNTS[r],float(COUNTS[r])/float(SUM)
            
    print "TOTAL", SUM
    

def predict_arm(x):
    h = hashlib.sha256(x["clientId"] + "tls13-comparison-all-v1@mozilla.org")
    v = (struct.unpack(">L", h.digest()[0:4])[0])
    variate = v/ 0xffffffff
    if variate < 0.5:
        return "treatment"
    else:
        return "control"


def tls_exp_handle_ping(accums, p):
    try:    
        if p["payload"]["status"] != "report":
           return
 
        results = p["payload"]["results"]
        for res in results:
            if "status" in res and res["status"] == 200:
                accums[res["url"]]["success"].add(1)
            else:
                accums[res["url"]]["failure"].add(1)
    except:
        accums["except"].add(1)
        pass

def tls_exp_results(pings):
    urls = [
        "https://enabled.tls13.com/",
        "https://disabled.tls13.com/",
        "https://short.tls13.com/",
        "https://control.tls12.com/"]
    accums = {}
    for u in urls:
        accums[u] = {
            "success":sc.accumulator(0),
            "failure":sc.accumulator(0),
        }
    accums["except"] = sc.accumulator(0)

    pings.foreach(lambda p: tls_exp_handle_ping(accums, p))

    results = {}
    for u in urls:
        results[u] = {
            "success": accums[u]["success"].value,
            "failure": accums[u]["failure"].value,
        }
    return [results, accums["except"].value]

def tls_exp_status(pings):
    accums = {
        "started":sc.accumulator(0),
        "report":sc.accumulator(0),
        "finished":sc.accumulator(0),
        "timedout":sc.accumulator(0),
    }
    pings.foreach(lambda p: tls_status_handle_ping(accums, p))
    return accums


def tls_status_handle_ping(accums, p):
    try:
        accums[p["payload"]["status"]].add(1)
    except:
        pass
    
def foo():
    print "FOO1"
