import sys

from enum import Enum
from typing import List, Dict, Set

if sys.version_info >= (3, 8):
    from typing import TypedDict 
else:
    from typing_extensions import TypedDict


class PublicationSource(Enum):
    '''
    Defines the source of the publication. In general, a publication 
    on Google Scholar has two forms:
    * Appearing as a PUBLICATION SNIPPET and
    * Appearing as a paper in an AUTHOR PAGE
    
    ------------
    
    "PUBLICATION SEARCH SNIPPET". 
    This form captures the publication  when it appears as a "snippet" in 
    the context of the resuls of a publication search. For example:
    
    Publication search: https://scholar.google.com/scholar?hl=en&q=adaptive+fraud+detection&btnG=&as_sdt=0%2C33
    
    The entries appear under the <div class = "gs_r gs_or gs_scl"> tags
    Each entry has a data-cid attribute (e.g., data-cid="pthm1bWT96oJ")
    
    The same type of results will also appear when someome searches 
    using the "cited by", "related articles", and "all XX versions" links
    that appear under the publication snippet.
    
    "Cited By" link: https://scholar.google.com/scholar?cites=12319477714873931942&as_sdt=5,33&sciodt=0,33&hl=en
    
    "Related Articles" link: https://scholar.google.com/scholar?q=related:pthm1bWT96oJ:scholar.google.com/&scioq=adaptive+fraud+detection&hl=en&as_sdt=0,33
    
    "All versions" link: https://scholar.google.com/scholar?cluster=12319477714873931942&hl=en&as_sdt=0,33
    
    The snippet version of these publications contain the information that appears in the results.
    Often, the snippet version will miss authors, will have an abbreviated name for the venue, and so on.
    
    We can fill these snippets by clicking on the "Cite" button" and get back the MLA/APA/Chicago/... 
    citations forms, PLUS links for BibTeX, EndNote, RefMan, and RefWorks.
    
    ------------
    "AUTHOR PUBLICATION ENTRY"
    
    We also have publications that appear in the "author pages" of Google Scholar. 
    These publications are often a set of publications "merged" together. 
    
    The snippet version of these publications conains the title of the publication,
    a subset of the authors, the (sometimes truncated) venue, and the year of the publication
    and the number of papers that cite the publication.
    
    The snippet entries appear under the <tr class="gsc_a_tr"> entries in the main page of the author.
    
    To fill in the publication, we open the "detailed view" of the paper
    
    Detailed view page: https://scholar.google.com/citations?view_op=view_citation&hl=en&citation_for_view=-Km63D4AAAAJ:d1gkVwhDpl0C
    '''
    PUBLICATION_SEARCH_SNIPPET = 1
    AUTHOR_PUBLICATION_ENTRY = 2
    
class AuthorSource(Enum):
    '''
    Defines the source of the HTML that will be parsed.
    
    Author page: https://scholar.google.com/citations?hl=en&user=yxUduqMAAAAJ
    
    Search authors: https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=jordan&btnG=
    
    Coauthors: From the list of co-authors from an Author page
    '''
    AUTHOR_PROFILE_PAGE = 1
    SEARCH_AUTHOR_SNIPPETS = 2
    CO_AUTHORS_LIST = 3
    


class BibEntryCitation(TypedDict):
    '''
    The bibliographic entry for a publication

    :param title: title of the publication
    :param authors: the names of the authors that contributed to this publication
    :param journal: Journal Name
    :param abstract: description of the publication
    :param pub_year: The year the publication was first published
    :param eprint: digital version of the Publication
    :param volume: number of years a publication has been circulated
    :param number: NA number of a publication
    :param pages: number of pages of a publication
    :param url: url where the publication is posted
    :param publisher: the Publisher of the Publication
    :param cites_id: This corresponds to a "single" publication on Google Scholar. Used in the web search
                       request to return all the papers that cite the publication. If cites_id = 
                       16766804411681372720 then:
                       https://scholar.google.com/scholar?cites=<cites_id>&hl=en
                       If the publication comes from a "merged" list of papers from an authors page, 
                       the "citedby_id" will be a comma-separated list of values. 
                       It is also used to return the "cluster" of all the different versions of the paper.
                       https://scholar.google.com/scholar?cluster=16766804411681372720&hl=en
    :param cites: number of citations of this publication
    '''
    title: str
    authors: str
    journal: str
    abstract: str
    pub_year: str
    eprint: str
    # pub_type: str # journal, conference, chapter, book, thesis, patent, course case, other ...
    volume: str
    number: str
    pages: str
    url: str
    publisher: str  
    cites_id: int # same thing as id
    cites: int

''' Lightweight Data Structure to keep distribution of citations of the years '''
CitesPerYear = Dict[int, int]


class PublicationCitation(TypedDict):
    """
    :param BibEntryCitation: contains additional information about the publication
    :param citedby_id: This corresponds to a "single" publication on Google Scholar. Used in the web search
                       request to return all the papers that cite the publication. 
                       https://scholar.google.com/scholar?cites=16766804411681372720hl=en
                       If the publication comes from a "merged" list of papers from an authors page, 
                       the "citedby_id" will be a comma-separated list of values. 
                       It is also used to return the "cluster" of all the different versions of the paper.
                       https://scholar.google.com/scholar?cluster=16766804411681372720&hl=en
    :param cites_per_year: a dictionay containing the number of citations per year for this Publication
    :param filled: whether the publication is fully filled or not
    :param author_pub_id: The id of the paper on Google Scholar from an author page. Comes from the 
                          parameter "citation_for_view=PA9La6oAAAAJ:YsMSGLbcyi4C". It combines the 
                          author id, together with a publication id. It may corresponds to a merging
                          of multiple publications, and therefore may have multiple "citedby_id" 
                          values.
    :param source: source of publication can either be `scholar` or `citation`
    :param container_type: Type of this Dictionary (Publication)

    """
    bib: BibEntryCitation
    citedby_id: str #citations_link
    cites_per_year: CitesPerYear
    filled: bool
    author_pub_id: str # id_citations
    source: str
    container_type: str


class BibEntryScholar(TypedDict):
    '''
    The bibliographic entry for a publication

    :param ENTRYTYPE: the type of entry for this bib (for example 'article')
    :param ID: bib entry id
    :param abstract: description of the publication
    :param title: title of the publication
    :param author: list of author the author names that contributed to this publication
    :param author_id: list of the corresponding author ids of the authors that contributed to the Publication 
    :param pub_year: the year the publication was first published
    :param year: the year the publication was first published
    :param eprint: digital version of the Publication
    :param venue: the venue of the publication
    :param journal: Journal Name
    :param volume: number of years a publication has been circulated
    :param number: NA number of a publication
    :param pages: range of pages
    :param publisher: The publisher's name
    :param gsrank: position of the publication in the query
    :param url: url of the website providing the publication
    :param cites: number of citations of this Publication
    '''

    ENTRYTYPE: str
    ID: str 
    abstract: str
    title: str
    author: str
    author_id: List[str]
    year: str
    eprint: str
    venue: str
    journal: str
    volume: str
    number: str
    pages: str
    publisher: str  
    gsrank: int
    url: str
    cites: int


class PublicationScholar(TypedDict):
    """
    :class:`Publication <Publication>` object used to represent a publication entry on Google Scholar.
    
    :param cites: number of citation for this publication
    :param citedby_id: This corresponds to a "single" publication on Google Scholar. Used in the web search
                       request to return all the papers that cite the publication. 
                       https://scholar.google.com/scholar?cites=16766804411681372720hl=en
                       If the publication comes from a "merged" list of papers from an authors page, 
                       the "citedby_id" will be a comma-separated list of values. 
                       It is also used to return the "cluster" of all the different versions of the paper.
                       https://scholar.google.com/scholar?cluster=16766804411681372720&hl=en
    :param related_id: Used to return the related papers for the given publication (also called "data-cid")     
    :param bib: The bibliographic entry for the page
    :param source: The source of the publication entry TODO corresponds to 
    :param filled: The Publication filled with additional information
    :param url_add_sclib: 
    :param url_scholarbib: the url containing links for the BibTeX entry, EndNote, RefMan and RefWorks
    """
    citedby_id: str # citations_link
    bib: BibEntryScholar
    source: str
    filled: bool
    url_add_sclib: str
    url_scholarbib: str
    container_type: str

class BibEntry(TypedDict, total=False):
    """
    The bibliographic entry for a publication

    :param ENTRYTYPE: the type of entry for this bib (for example 'article') (1)
    :param ID: bib entry id (1)
    :param abstract: description of the publication
    :param title: title of the publication
    :param author: list of author the author names that contributed to this publication
    :param pub_year: the year the publication was first published
    :param eprint: digital version of the Publication. Usually it is a pdf.
    :param venue: the venue of the publication
    :param journal: Journal Name
    :param volume: number of years a publication has been circulated
    :param number: NA number of a publication
    :param pages: range of pages
    :param publisher: The publisher's name
    :param url: url of the website providing the publication
    """
    pub_type: str
    bib_id: str
    abstract: str
    title: str
    author: str
    pub_year: str
    eprint: str # TODO: this should represent url
    venue: str
    journal: str
    volume: int
    number: int
    pages: str
    publisher: str  
    url: str


class Publication(TypedDict, total=False):
    """
    :param BibEntryCitation: contains additional information about the publication
    :param gsrank: position of the publication in the query (1)
    :param author_id: list of the corresponding author ids of the authors that contributed to the Publication (1)
    :param num_citations: number of citations of this Publication
    :param cites_id: This corresponds to a "single" publication on Google Scholar. Used in the web search
                       request to return all the papers that cite the publication. If cites_id = 
                       16766804411681372720 then:
                       https://scholar.google.com/scholar?cites=<cites_id>&hl=en
                       If the publication comes from a "merged" list of papers from an authors page, 
                       the "citedby_id" will be a comma-separated list of values. 
                       It is also used to return the "cluster" of all the different versions of the paper.
                       https://scholar.google.com/scholar?cluster=16766804411681372720&hl=en
                       (2)
    :param citedby_id: This corresponds to a "single" publication on Google Scholar. Used in the web search
                       request to return all the papers that cite the publication. 
                       https://scholar.google.com/scholar?cites=16766804411681372720hl=en
                       If the publication comes from a "merged" list of papers from an authors page, 
                       the "citedby_id" will be a comma-separated list of values. 
                       It is also used to return the "cluster" of all the different versions of the paper.
                       https://scholar.google.com/scholar?cluster=16766804411681372720&hl=en (both)
    :param cites_per_year: a dictionay containing the number of citations per year for this Publication (2)
    :param author_pub_id: The id of the paper on Google Scholar from an author page. Comes from the 
                          parameter "citation_for_view=PA9La6oAAAAJ:YsMSGLbcyi4C". It combines the 
                          author id, together with a publication id. It may corresponds to a merging
                          of multiple publications, and therefore may have multiple "citedby_id" (2)
                          values.
    :param url_add_sclib: (1)
    :param url_scholarbib: the url containing links for 
                           the BibTeX entry, EndNote, RefMan and RefWorks (1)
    :param filled: whether the publication is fully filled or not
    :param source: The source of the publication entry TODO corresponds to 
    """

    bib: BibEntry
    gsrank: int # TODO: should be moved
    author_id: List[str]
    num_citations: int # TODO: change name to num_citations
    cites_id: int # same thing as id
    citedby_id: str # TODO: change to link
    cites_per_year: CitesPerYear
    author_pub_id: str # id_citations
    url_add_sclib: str
    url_scholarbib: str
    filled: bool
    source: PublicationSource # Change to publication enum
    container_type: str

class Author(TypedDict):
    """
    :class:`Author <Author>` object used to represent an author entry on Google Scholar.
    
    :param scholar_id: The id of the author on Google Scholar
    :param name: The name of the author
    :param affiliation: The affiliation of the author
    :param email_domain: The email domain of the author
    :param url_picture: The URL for the picture of the author
    :param citedby: The number of citations to all publications.
    :param filled: The set of sections filled out of the total set of sections that can be filled
    :param interests: Fields of interest of this Author
    :param citedby5y: The number of new citations in the last 5 years to all publications.
    :param hindex: The h-index is the largest number h such that h publications have at least h citations
    :param hindex5y: The largest number h such that h publications have at least h new citations in the last 5 years
    :param i10index: This is the number of publications with at least 10 citations.
    :param i10index5y: The number of publications that have received at least 10 new citations in the last 5 years. 
    :param cites_per_year: Breakdown of the number of citations to all publications over the years
    :param publications: A list of publications objects
    :param coauthors: A list of coauthors (list of Author objects)
    :param container_type: The type of this dictionary
    """

    scholar_id: str
    name: str
    affiliation: str
    email_domain: str
    url_picture: str
    citedby: int
    filled: Set
    interests: List[str]
    citedby5y: int
    hindex: int
    hindex5y: int
    i10index: int
    i10index5y: int
    cites_per_year: CitesPerYear
    publications: List[PublicationCitation]
    coauthors: List
    container_type: str
