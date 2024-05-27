from uuid import UUID

"""
The UUIDs are used as an indirect mapping to enable easier changing on names. Otherwise we would have to change every occurrence.
"""


class ActionIDs:
    BEATMUNG = UUID("154a9717-640a-4c6e-bae3-605a32c75673")
    THORAXDRAINAGE = UUID("23da8633-a4a6-4af2-a0cb-4b34540033d4")
    PLEURAPUNKTION = UUID("22b66af8-ace9-4652-a69c-be62425311cb")
    TRACHEALTUBUS = UUID("25fba4ad-b2fe-4761-87e7-5d5401ac359b")
    LARYNXMASKE = UUID("9883a5c0-300f-4e71-ad7d-fc64d46274f0")
    LARYNXTUBUS = UUID("234d0237-ffa0-4e27-b269-99b39f6bfd9f")
    GUEDELTUBUS = UUID("8c3870ce-8cf6-47a7-add0-734fefaed093")
    WENDELTUBUS = UUID("59edf7ba-7f05-4669-bed7-c17c9ffaccd0")
    KONIOTOMIETUBUS = UUID("0c182ca3-323d-48ae-80f2-5b4dfb914917")
    ANALGETIKUM = UUID("e23f9c72-32fc-4a3f-806a-3031943e145d")
    ANTIASTHMATIKUM = UUID("50014ee9-750a-4fb1-b8b1-50b4f05548c9")
    KORTIKOSTEROID = UUID("a3bf5f18-a24f-429a-a28a-fef9ad85e26b")
    NITRAT = UUID("b3d54ebc-1459-4e8b-8c4e-98a3c68b1607")
    DIURETIKUM = UUID("c76527e0-c069-4036-a44c-cfe6b085460e")

    KATECHOLAMIN = UUID("2918f983-a88d-4d87-9050-c1232223a9c7")
    SEDATIVUM = UUID("2aef024b-b013-490b-87d5-95d9fe10ed72")
    REGIONAL_NARKOTIKUM = UUID("6b826d26-aa0a-4317-96f5-6565d7ee1e5f")
    TETANUSPROPHYLAXE = UUID("d3969915-f09c-4a1d-a0b1-b39dea503b20")
    ANTIKOAGULANZ = UUID("1b3ee4c4-892d-47e5-b95c-d2aa5b17f21a")
    NARKOTIKUM = UUID("2de49d83-11be-410c-ac7a-68c458baf620")
    VOLLELEKTROLYT = UUID("2f1b5a58-57a8-4ba9-bb6d-69d2155cdf4d")
    PLASMAEXPANDER = UUID("8b14fef8-4cb1-40b7-88ff-2e15fc28b72f")
    IV_ZUGANG = UUID("7613f009-cb28-411d-91a9-26fe438a3bc2")
    ZVK = UUID("0497f5cb-bb98-42f1-a259-e6d59e2582a4")
    SCHLEUSE = UUID("3c5dbce0-ec74-4b3e-a4b7-45b74b8b3bb0")
    ART_KANUELE = UUID("c62f3077-637b-4a09-b428-d2098403c6f3")
    MEHRLUMEN_ZVK = UUID("57f5ff1e-e592-4e6b-9659-fce010c839e8")
    REGIONAL_NARKOSE = UUID("d4971ae5-117b-49b8-b5c9-4e4220ff971c")
    ZVD = UUID("a3b8c362-1b5d-49b9-a1c4-a76b4cb46797")

    DRUCKVERBAND = UUID("cc8a5284-765d-4854-b634-6c9e5a85d916")
    TURNIQUET = UUID("8fb0f831-6335-40ab-b8e3-5b0afa9e975c")
    WUNDVERSORGUNG = UUID("d4b761a3-d5e6-4f0b-a584-414a3e7a4a95")
    CHIR_BLUTSTILLUNG = UUID("0f5fef5b-998c-4648-a93e-9a6e8ccad3b7")
    STIFNECK = UUID("4f6f992c-a324-4717-a6b6-eae3b347c208")
    VAKUUMSCHIENE = UUID("7e5ae52b-421b-4977-a787-53c0d3a0bf22")
    BECKENSCHLINGE = UUID("9dcb3a4b-5dca-4602-bb0a-66a935a29c8d")
    GIPSVERBAND = UUID("e0b3938d-86af-41d5-a7da-550c0a9e5a25")
    STABILE_SEITENLAGE = UUID("aaf04c59-6c34-4a60-9d67-1a007f015c30")
    SCHOCKLAGE = UUID("0c7f9661-b2b6-4760-aa6d-4c53858289b6")
    DEFI_TRANSCUTANER_PACER = UUID("9d1db5ee-3b28-4c8f-8a89-751f684d8cd6")
    BEATMUNGSGERAET_ANBRINGEN = UUID("72d6f3ad-b9a5-4b16-b289-815766b27c4f")
    SAUERSTOFF_ANBRINGEN = UUID("7b4861b2-e775-4d2a-9cd5-26bab7cc76a0")
    BLUTDRUCK_MESSGERAET_ANBRINGEN = UUID("38d8ce9d-8cf8-4f85-9ee8-ae8856bb28d4")
    SAETTIGUNGSMESSGERAET_ANBRINGEN = UUID("2c673f7a-9aa1-4127-b060-2c392fa0a60b")
    MONITOR_ANBRINGEN = UUID("71d6dd05-fd24-427f-bc70-5120e14cbeb7")
    PASSAGEREN_PACER_ANBRINGEN = UUID("9b498c06-3b76-4028-9a24-23958cbef9e2")
    PERFUSORPUMPE_AKTIVIEREN = UUID("8ec3fcec-042b-49b5-a5b4-8354c5d0801b")
    PERFUSORPUMPE_MIT_WIRKSTOFF_BESTUECKEN = UUID(
        "9fcacc50-5c54-42ee-acd3-6f617b0c342e"
    )
    GLUCOSE_VERABREICHEN = UUID("1d6b0f2e-7efb-4065-9d58-ff52320e3c7c")
    LYSE_VERARBREICHEN = UUID("baaf316b-0565-4056-8d31-8c5595d24475")
    PATIENT_IN_BENACHBARTE_STATION_VERSCHIEBEN = UUID(
        "5d3138a7-a4f3-47ff-839b-7852a271b902"
    )
    GERAET_IN_ANDERE_STATION_VERSCHIEBEN = UUID("1ea079b5-e3cb-4f14-a6e6-c13900e2c4ed")
    FRESH_FROZEN_PLASMA_AUFTAUEN = UUID("3c3a2f24-8a8e-4c59-9b5f-89d8a5bc5677")
    LYOPHILISIERTES_FRISCHPLASMA_AUFLOESEN = UUID(
        "bf4c6cd9-6ee1-4b43-aa71-a9f6939b7cdf"
    )
    BLUTGASEANALYSE_FUER_OXYGENIERUNGSLEISTUNG = UUID(
        "ce492b24-cf12-42b5-a674-d3c77d463f12"
    )
    BLUTGASEANALYSE_FUER_SAEURE_BASE_HAUSHALT = UUID(
        "e5751d05-95c8-4b89-bc6b-1ded08db3a16"
    )
    BLUTZUCKER_ANALYSIEREN = UUID("2e55b5e0-d07e-4f88-9c59-245c6a3b0f23")
    EKG_ANBRINGEN = UUID("d8b9656d-d8f7-4cdd-a4b9-3e7f31a3b5a3")
    EKG_ABLESEN = UUID("4295621b-ae8b-419a-b8ea-e9c0a2a80f2e")
    ZENTRALEN_VENENDRUCK_MESSEN = UUID("fcabd1bc-bb0b-4ac1-9dde-e1e661ecb9e5")
    EXTREMITAETEN_ROENTGEN = UUID("f9c3fdaa-5a7f-426d-94d8-0d78400a835a")
    THORAX_ROENTGEN = UUID("50dab612-2d76-48d1-98a2-8764f154123f")
    TRAUMA_CT = UUID("9f442b68-736f-4117-9c0e-f1f0ec26a1c2")
    ULTRASCHALL_ABDOMEN = UUID("7c4f983d-760f-45aa-9dce-5ae8b244c782")
    ULTRASCHALL_THORAX = UUID("ba8d69fa-3d0e-46c6-afd0-eb2aebb0bd6a")
    KREUZBLUT = UUID("d1c8d943-1ee7-451d-925e-5398fcab9e8f")
    BLUTGRUPPE_BESTIMMEN = UUID("1c048b94-a034-494b-8444-59c641a1c291")
    HAEMOGLOBINANALYSE = UUID("a78ce77f-96da-403a-b3d9-a5f77b0816cd")
    LACTATANALYSE = UUID("35872dae-733f-408d-bf55-a1c1e1e3bdbf")
    GERINNUNGSANALYSE = UUID("1c76a608-1a25-4987-8621-74f697c2b90d")
    LEBERANALYSE = UUID("4859bbaa-df71-4d2b-9587-68b644b5c5c7")
    NIERENANALYSE = UUID("6a3e7330-a4bf-4721-83c2-fab0db9307c1")
    INFARKTANALYSE = UUID("2179fba5-e8cf-489b-aa33-7e036b92c8d3")
    FRESH_FROZEN_PLASMA_ANWENDEN = UUID("87403e5c-3031-45d2-85ad-a1a5ea7cc81c")
    ENTHROZYTENKONZENTRATE_ANWENDEN = UUID("f3b502a4-0c3d-4a9f-a829-e0a59a067c53")
    ENTHROZYTENKONZENTRATE_JEGLICHE_BLUTGRUPPE_ANWENDEN = UUID(
        "b5f4c015-4152-459f-bdbb-defab91a3d99"
    )


class MaterialIDs:
    # TODO: add UUIDable mixin to Material models once it exists
    ENTHROZYTENKONZENTRAT_0_POS = UUID("f6576558-c1d3-4548-823b-2c1e2b0636d7")
    BLUTAUFTAU_SLOT = UUID("d8d0a768-c7de-40bb-94d2-2d495e911aec")
    BEATMUNGSGERAET = UUID("bd466499-6aeb-4a36-8687-04711b001139")
    BEATMUNGSBEUTEL = UUID("9ddcbe2f-0c95-4562-8dc9-3e9ab990a526")
    SPRITZENPUMPE = UUID("4f452e8b-ceaf-423d-9a14-04c08217fe99")
    DEFIBRILATOR = UUID("d8759a11-faa0-42ea-a127-9e24d376f857")
    WAERMEGERAET_FUER_BLUTPRODUKTE = UUID("2ccbae94-b539-4227-ab2c-8cbc15470604")
    BGA_GERAET = UUID("2ea085df-fc13-492f-822c-e44d634247e5")
    EKG_GERAET = UUID("e6d9e9f3-7b0e-4a5a-8b1b-3e8a1e2f1c2d")


class RoleIDs:
    PFLEGEFACHKRAFT = UUID("14c0946d-d06c-4c44-a2ad-71625ec1fc6c")
    ARZT = UUID("59ff24ae-9298-4a1b-88c7-5366e011f77d")
    LABORASSISTENT = UUID("66056789-afee-4c1d-9044-a7966ab3b15b")
    HILFSKRAFT = UUID("46d91d1c-cd86-4953-a2ef-370f20987ef2")
    MTRA = UUID("9ac54833-f1eb-4175-a8e9-64cd6c681b16")


role_map = {
    RoleIDs.PFLEGEFACHKRAFT: "Pflegefachkraft",
    RoleIDs.ARZT: "Arzt",
    RoleIDs.LABORASSISTENT: "Laborassistent",
    RoleIDs.HILFSKRAFT: "Hilfskraft",
    RoleIDs.MTRA: "Medizinisch Technische Röntgen Assistentin",
}


class ActionResultIDs:
    HB420 = "9f878489-07fc-41a4-8979-f3e9c8e7e9b7"
    HB430 = "4a76bb8d-ccd2-4f27-9e08-3131ed3c0178"
    BZ920 = "3ddade44-701a-43b9-9670-a8e346a45048"
    BZ930 = "c30d670e-c072-4263-9f6a-895d00ef7368"
