from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "sessions" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
        COMMENT ON COLUMN "users"."activity_level" IS 'SEDENTARY: sedentary
LIGHTLY_ACTIVE: lightly_active
MODERATELY_ACTIVE: moderately_active
VERY_ACTIVE: very_active
EXTRA_ACTIVE: extra_active
ATHLETE: athlete';
        COMMENT ON COLUMN "exercises"."intensity" IS 'LOW: low
MODERATE: moderate
MEDIUM: medium
HIGH: high
VERY_HIGH: very_high';
        ALTER TABLE "exercises" ALTER COLUMN "name" TYPE VARCHAR(31) USING "name"::VARCHAR(31);
        COMMENT ON COLUMN "exercises"."name" IS 'ABDOMINAL: abdominal
ABDOMINAL_INVERTIDO: abdominal_invertido
ABDOMINAL_NA_POLIA: abdominal_na_polia
AGACHAMENTO: agachamento
AGACHAMENTO_BULGARO: agachamento_bulgaro
AGACHAMENTO_FRONTAL: agachamento_frontal
AGACHAMENTO_GOBLET: agachamento_goblet
AGACHAMENTO_HACK: agachamento_hack
AGACHAMENTO_PISTOLA: agachamento_pistola
AGACHAMENTO_SUMO: agachamento_sumo
AGACHAMENTO_ZERCHER: agachamento_zercher
ARRANCADA: arrancada
BARRA_FIXA: barra_fixa
BARRA_FIXA_PEGADA_LARGA: barra_fixa_pegada_larga
BARRA_FIXA_SUPINADA: barra_fixa_supinada
BARRA_FIXA_COM_PESO: barra_fixa_com_peso
BURPEE: burpee
CADEIRA_ABDUTORA: cadeira_abdutora
CADEIRA_ADUTORA: cadeira_adutora
CAMINHADA_DO_FAZENDEIRO: caminhada_do_fazendeiro
CRUCIFIXO: crucifixo
CRUCIFIXO_INVERSO: crucifixo_inverso
CRUCIFIXO_NA_POLIA: crucifixo_na_polia
DESENVOLVIMENTO: desenvolvimento
DESENVOLVIMENTO_ARNOLD: desenvolvimento_arnold
DESENVOLVIMENTO_COM_HALTERES: desenvolvimento_com_halteres
DESENVOLVIMENTO_FRONTAL: desenvolvimento_frontal
ELEVACAO_FRONTAL: elevacao_frontal
ELEVACAO_LATERAL: elevacao_lateral
ELEVACAO_LATERAL_CURVADO: elevacao_lateral_curvado
ELEVACAO_NA_PANTURRILHA: elevacao_na_panturrilha
ELEVACAO_NA_PANTURRILHA_SENTADO: elevacao_na_panturrilha_sentado
ELEVACAO_PELVICA: elevacao_pelvica
ENCOLHIMENTO: encolhimento
ESCALADOR: escalador
EXTENSAO_DE_COSTAS: extensao_de_costas
EXTENSAO_DE_PERNAS: extensao_de_pernas
EXTENSAO_DE_TRICEPS: extensao_de_triceps
FACE_PULL: face_pull
FLEXAO: flexao
FLEXAO_DIAMANTE: flexao_diamante
FLEXAO_DE_PERNAS: flexao_de_pernas
GOOD_MORNING: good_morning
LEG_PRESS: leg_press
LEVANTAMENTO_TERRA: levantamento_terra
LEVANTAMENTO_TERRA_DEFICIT: levantamento_terra_deficit
LEVANTAMENTO_TERRA_ROMENO: levantamento_terra_romeno
LEVANTAMENTO_TERRA_STIFF: levantamento_terra_stiff
LEVANTAMENTO_TERRA_UMA_PERNA: levantamento_terra_uma_perna
MERGULHO_NO_BANCO: mergulho_no_banco
MERGULHO_PARALELA: mergulho_paralela
MUSCLE_UP: muscle_up
PANTURRILHA_EM_PE: panturrilha_em_pe
PECK_DECK: peck_deck
POLICHINELO: polichinelo
PRANCHA: prancha
PRANCHA_LATERAL:';
        ALTER TABLE "exercises" ALTER COLUMN "type" TYPE VARCHAR(11) USING "type"::VARCHAR(11);
        COMMENT ON COLUMN "exercises"."type" IS 'BACK: back
CHEST: chest
LEGS: legs
ARMS: arms
SHOULDERS: shoulders
ABDOMEN: abdomen
CARDIO: cardio
STRENGTH: strength
FLEXIBILITY: flexibility
SPORTS: sports';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        COMMENT ON COLUMN "users"."activity_level" IS 'SEDENTARY: sedentary
LIGHTLY_ACTIVE: lightly_active
MODERATELY_ACTIVE: moderately_active
VERY_ACTIVE: very_active
EXTRA_ACTIVE: extra_active';
        COMMENT ON COLUMN "exercises"."intensity" IS 'LOW: low
MEDIUM: medium
HIGH: high
VERY_HIGH: very_high';
        ALTER TABLE "exercises" ALTER COLUMN "name" TYPE VARCHAR(255) USING "name"::VARCHAR(255);
        COMMENT ON COLUMN "exercises"."name" IS NULL;
        COMMENT ON COLUMN "exercises"."type" IS 'BACK: back
CHEST: chest
LEGS: legs
ARMS: arms
SHOULDERS: shoulders
ABDOMEN: abdomen';
        ALTER TABLE "exercises" ALTER COLUMN "type" TYPE VARCHAR(9) USING "type"::VARCHAR(9);
        DROP TABLE IF EXISTS "sessions";"""


MODELS_STATE = (
    "eJztXetv2zgS/1cMf+oCvW7TdtttcDhAsRVbV9kyZDntdrMQaIm2eZFIrR55bNH//YZ6P1"
    "PbSZq45Zc2Hs5Q5G+Gw5khLX/pu8zGTvBiEWC/f9z70qfIxfBHhf6810eeV1A5IURLJ2aM"
    "gCOmoGUQ+sgKgbhCToCBZOPA8okXEkaBSiPH4URmASOh64IUUfJ3hM2QrXG4iQfy519AJt"
    "TG1zjIPnoX5opgx66Mk9j82THdDG+8mLZYKMPTmJM/bmlazIlcWnB7N+GG0Zw9ioj9gsvw"
    "tjWm2EchtkvT4KNMp5uRkhEDIfQjnA/VLgg2XqHI4WD0/72KqMUx6MVP4v+8+U9/B3gsRj"
    "m0hIYciy9fk1kVc46pff6owVjSn71++0s8SxaEaz9ujBHpf40FUYgS0RjXAkjsIuI0sRxs"
    "kN+OZS5QgxOG+jBAZgDth1rfRdemg+k63MDHV7/9dguMZ5IeIwlcMZQM7Dqx9mna9Cpp45"
    "AWEMb/74Bgxn8/AGaEAsFiGR4MhBsUbLBteigIrpjfsra70WwRFcDmwC6JH25MWP0tFjoE"
    "ajumVakanJwcEhe/yNqfHrC34DiUDLmGkc+cjvUr08iNEVKge0Qt3EAqk/1+JhfvvM1tpL"
    "+Yy/pxjzeeU2k4UabHPWS7hPb3MMVtDLHbDJurG5P1JjQtt4nyqcNQ2LGwy1I1fFdc7KEQ"
    "fvni5cOYnrY4UeXeTJcHylzRpnz87k3wt1M0chIQSBjPUpcltQblmqGW3foWFDOBPQFMd+"
    "MnsnbvA0AMI/f3Xe6F9CPvMf2JpMrHPRc5+JyeysmnFeaf91nwb7dY8G87F/zb+oKHdIBc"
    "kvAGHnCJO6LLb4Pd7OWxQZ/LQ3lqSPofx70A25iGyL85p6oyGhvqH6Y0MJQzUIPD/ZZzY8"
    "bjB/VMtKGsw7ZTYuEJFR9yietM1ov2S+wXLfInQ5fyJnwNWszbJGOsygaQUbhxcLiX8o/e"
    "baH9o3ed6udNLfqH6QVm4mSacQcPINodVl32tuiD/3FoTsxQJvLckCaz2HsFmfcC++Atr6"
    "o+LaU21l7eSe+jYox7/GPvszaV6wlgzmd87vMxoShkJmVXJrLL087IGamiTMvHHNo9VFmV"
    "vAdFPkaMDnOwNercpHZ0IJpNTf5WxUaevadiq5JCsY+q2HjwvFC2uihVeDhhiayLK+TbZq"
    "WlMADIly9YFAZN9Z+kkqcfdOygGNqmotNa4cekl6ep5a+Z6WbUQtulJJnZsNsGAQ4CF9O7"
    "4nECvUl5ZwcMi4Uc5hPLhGZ0ge+IyiDpTIn7OmBQuF6h3zuiMU96OTAcuE9hr1iXl2k2ua"
    "/cOgVRtI5HzZ/Nn1TzIi2HESUH030eUfZl4kjioI8kRD39zmXfGINWCL+ddmeyj51sDyR9"
    "qGjHPQt8C2HndG7o8nRkjCH3Dv0YvXN6qsqflBNFVQxIyVcOviZL4pAQkvITSZWmA0iMl8"
    "jJp7lrYny0TWJ81J0YHzX0wkLkmMnGChnuMvIpbnEbt9TzOnsQFdJ0gw6RH5pZ3rFLVlOV"
    "PMys5kCymK0KD5jae+mxLCeqR0+ierR38UiUGJ5CiaGldhRg39wt4i2J3GfY+6jL8RtRbq"
    "MqUwWwZeNnPiZr+gHfNGK09kQyu6j1ZFFrZJFA9tFVnj+VzQKmB5PCydY+kOYDaSj3v25T"
    "yYI5+BYJ7lqkkJNugifqTx4lMS8waUnNK4B1J+cV9Yjs/AfNzr+dWj6RTL0vnQy1iTKV1O"
    "MeWtrMJRQ55zSnmsr0TNYNZaiV2k1CL7EfEpuVOaeSOdNURSozUmR6zCEI+EYSID2Rpwbv"
    "aY2sDeI1YVZpMU8W6kjSqxyQ2Dlr5Nc4T3VtasSjLnGufEbDePwlzpEGuZJRZVwzADKs8o"
    "2lwYcq1wa8RpVnpswNTZWqbB4JQuZU52jOF5PaNILIrc3hswzZMb+qVGb7B/zDJr65pOuQ"
    "tktD/jTfByNCNuLJPJDNU+WTxPN5oINlXlfo5kwegZSpSvqowmR6eA19mA7y11WJ+WIGKh"
    "xWuYPIAx1Wn2kOtAn0P9cqnBZzoe8AZney0GcyrzREvofxOeXblsJP7E+GC0PTJV7CsDHh"
    "p/ZLG4IqH5V4GiwFB1jYmM9pCIqXPstTLhHXQ8DMNnxONigf/cOvpBBuKQN9MVBgwJzHjy"
    "wCwyxTE6uel1sTmw4qXIVFF2yFRQ/luTw909QzJbVqWFmYXjLnkqSWXeMwJX2qqcMGo4l8"
    "yhy7yc/BHkuqIevyvCnFUd8gJ8TgsJqy+fqoi+VrRFblM2kglVgh4LhEFmrjUSHQ1is8EE"
    "CAi2rhMQcL/UziDqPOa1qRf4m418hlOMTS1FjouqKOpZIIxxnRMPJ94mxQp4Q557dQKg+r"
    "SpoBv5tSeeZMBpQG5Yd5GOCx+FOmA00dZwrFFPz1JtOmDEGYCo+C9QouFDnQqR/fSJGnc+"
    "h1KIO+IJWYx/dSMA2gXxuDlmADCKp8M1mf1vk87NM6n6ErA3lWY4SNzsIecJ5KA+hqoarc"
    "2VvQA/j3pAwoaUkFELHsszlUpAmgJmcNpk0QxDkhLjiKcWUsxahGmjY0J5o+Vaaj496aMd"
    "t0mU9hyz2nqjwyZ2ChIOjgtemBOQacegbPSx0d2AVf2BxuUEZih2ARfG03+WAkp8pAMdr4"
    "YUwrYpGwVU7X4JPWKuYz+MRapeaGcnraKhSEZLVqlVlMpASsVrnIRQlw53Qi66OFOgarhb"
    "0NvDmMzsX+OnI2PJ80l+DVWYlrJsH6kfn+knN5CBYO5rvLZDEfqLK5mEFrFECea0beOS2v"
    "BZn75uNe2fox98zAJQ8+AK58g/OwdQEw8p2NO7fBWJnKKoyLezVrQyh2YEQzvvXw9ejxjY"
    "evv5SSO4J9isivtykiv+4uIr9uFpF/gOL+SRx3LONYA8KBORg+BABBbOOjZFEFPBqYzHkg"
    "4MLf87G2UIewgR33gg2LHBs2rjQSk6dp+IUp3zfvcmwwn2m6wR/hMT85THz8QwN4DjhCGN"
    "6+Sq908NiaV7WPoF52VdyLLK5Dcq8wVBYT7gpsErnndKyMQHMbst6kNyQTQnw/klP30dD7"
    "LRT0vlM/7+vquctpjjjH6TzHEdcOf9DScXpTY8fqcVVKFJAzQO6hhnyQF/ie18rIVfvYv5"
    "Ic4Lve/5vjA4PyQcvHHI2WwnEKUnfJONODqBYfdLXYh6y9CaVCO+KhjL2GJdnqHu33P6iH"
    "EcF//3p19Obdm99fv33zO7DEQ8kpt321RpkatZjnKv7K404RZCEivuGXgGhHfu6htzS7ss"
    "hPanoiixFZjMhits9isiPtHdOYmpjIY3JE7iGROdDrG89rqUzNRnbNZR4ymq99t6klsG9+"
    "+6k7xm/73pWI9w863k/CUfNivUcQm0p9z9ChvUQ9wwHrxRfte5T1bIJ6NuqhS8RPwKOXL/"
    "G7+N/XbLvi8wNHGAf2cpWOCzlOCCE4R9tl8ali7xlx+REMP63t8ePAHrAjmsCPgl//xy4x"
    "DX55Ehq4QiTYWQFlIZG5paZMvJ3tOBcRIKYZBz9G3RXGspAAMr3oyO8M7IhjSUbAmL4Lxn"
    "d3RbEQESCmVz74WfeuMJaFBJAJkCsG3cbebicoq2ICzBKY+b3n3QGtiApQS6CG2d2W3QDN"
    "xQSYZTCTy6N7wFkICkBLgAbRMrCQFzmo7Sts3wC1JiyArQDrwQMdgqx9cC3LClhLsLrERt"
    "cEJum3XKH8Fq41YQFs+s6slbcTlim/gC+FzyW7wZfwC/gy+HbbeVJ+AV+aTtq47bztllQy"
    "FRAAJgA6GFHTRUGw60lHXVAAmu7TKNwLz5qcgFNcO/mhr52I966I9648+ntXHvKGSfU9sS"
    "0XTBovku2+X9LyAltxveSgr5fs+kNGP8tPGOU3cHkvkbvv/d2ytLjBm0Dr+SzEhJprH7m7"
    "1ZAbkgLSzFr9ZbAHoDU5AWeeO+2DZlVMgCkyJ5E5iczpucicDjRzyn5TovXbtvnPTdz2jd"
    "vily1EmnTQaZLYxH7QTQxfe8Tf62f1qpKHqdgDUWQ2bRGOiHDk5w1HJOwTa9MWjaQttwYj"
    "qOB5MqFI5+sDWtdky4sDUu3dLQS54954L68N6I48+OtkW9+90P3zTSUR8QtOxdcmvJb7Vd"
    "0gpuyHCeDRy5dbAAhc3S9N5G21Qg7jbz1siZP+O9emHcFvIVIDckFhgn/axAqf9xwShH89"
    "TVhvQZHPuhIbZeA9m0if6rgOVO2kviPzDk7atuTvub18/T82PlbZ"
)
