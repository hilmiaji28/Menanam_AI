CROP_MAPPING = {

    "padi": "Budidaya_Padi_ID.pdf",

    "jagung": "Budidaya_Jagung_ID.pdf",

    "singkong": "Budidaya_Singkong_ID.pdf",

}


def detect_filter(question: str):

    question = question.lower()

    for crop, source in CROP_MAPPING.items():

        if crop in question:

            return {
                "source": source
            }

    return None