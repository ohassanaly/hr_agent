from langchain_core.tools import tool


@tool("CV")
def cv_info(query: str) -> str:
    """Get some generic information about Olivier Hassanaly professional course checking its Curriculum content"""
    with open("about/cv_online.txt", "r", encoding="utf-8") as f:
        content = f.read()
    return content


@tool("linkedin")
def linkedin_info(query: str) -> str:
    """Get some extra information about Olivier Hassanaly professional milestones checking its Linkedin content"""
    with open("about/linkedin.txt", "r", encoding="utf-8") as f:
        content = f.read()
    return content


@tool("personal")
def personnal_info(query: str) -> str:
    """Get some extra information about Olivier Hassanaly personnal life"""
    with open("about/perso.txt", "r", encoding="utf-8") as f:
        content = f.read()
    return content
