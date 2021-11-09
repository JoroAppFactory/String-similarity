from strsimpy.cosine import Cosine


def distance(str1, str2):
    cosine = Cosine(2)
    p0 = cosine.get_profile(str1)
    p1 = cosine.get_profile(str2)
    return cosine.similarity_profiles(p0, p1)
