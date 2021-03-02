import importlib
import language as sqlang


# Gets sample for user's language
def get_sample(sample_name: str, name: str):

    sql_language = sqlang.Language(name)
    language = sql_language.get_language()

    language_samples = importlib.import_module(f"langs.{language.lower()}")
    samples = language_samples.Samples()

    # bruh
    try:
        sample = eval(f"samples.{sample_name}")
    except:
        language_samples = importlib.import_module("langs.english")
        samples = language_samples.Samples()
        sample = eval(f"samples.{sample_name}")

    return sample


