import requests
import json
import logging
from datetime import datetime
from django.conf import settings
from .models import Book

logger = logging.getLogger(__name__)

class OpenLibraryAPI:
    """
    Utility class for interacting with the Open Library API
    """
    BASE_URL = "https://openlibrary.org"
    SEARCH_URL = f"{BASE_URL}/search.json"
    WORK_URL = f"{BASE_URL}/works"
    BOOK_URL = f"{BASE_URL}/books"
    COVERS_URL = "https://covers.openlibrary.org/b"

    @classmethod
    def search_books(cls, query, page=1, limit=10, advanced_params=None):
        """
        Search for books using the Open Library Search API
        
        Parameters:
        - query: Search query string
        - page: Page number for pagination
        - limit: Number of results per page
        - advanced_params: Dictionary of additional search parameters
        
        Returns:
        - Dictionary containing search results and metadata
        """
        params = {
            'q': query,
            'page': page,
            'limit': limit,
        }
        
        # Add advanced search parameters if provided
        if advanced_params:
            params.update(advanced_params)
        
        try:
            response = requests.get(cls.SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process and format the results
            formatted_results = []
            for doc in data.get('docs', []):
                formatted_results.append(cls._format_search_result(doc))
            
            return {
                'results': formatted_results,
                'num_found': data.get('num_found', 0),
                'page': page,
                'limit': limit,
                'total_pages': (data.get('num_found', 0) + limit - 1) // limit
            }
        
        except requests.RequestException as e:
            logger.error(f"Error searching books: {str(e)}")
            return {
                'results': [],
                'num_found': 0,
                'page': page,
                'limit': limit,
                'total_pages': 0,
                'error': str(e)
            }

    @classmethod
    def get_book_details(cls, olid):
        """
        Get detailed information about a book using its Open Library ID
        
        Parameters:
        - olid: Open Library ID (can be work ID or edition ID)
        
        Returns:
        - Dictionary containing book details
        """
        # Determine if it's a work ID or edition ID
        is_work = olid.startswith('OL') and olid.endswith('W')
        is_edition = olid.startswith('OL') and olid.endswith('M')
        
        if not (is_work or is_edition):
            logger.error(f"Invalid Open Library ID format: {olid}")
            return None
        
        try:
            # Get the appropriate URL based on ID type
            if is_work:
                url = f"{cls.WORK_URL}/{olid}.json"
            else:
                url = f"{cls.BOOK_URL}/{olid}.json"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # If it's a work, we need to get an edition for more details
            if is_work and 'first_publish_date' in data:
                # Try to get the first edition
                editions_url = f"{cls.WORK_URL}/{olid}/editions.json"
                editions_response = requests.get(editions_url, params={'limit': 1})
                
                if editions_response.status_code == 200:
                    editions_data = editions_response.json()
                    if editions_data.get('entries') and len(editions_data['entries']) > 0:
                        # Merge work data with first edition data
                        edition_data = editions_data['entries'][0]
                        data.update(edition_data)
            
            # Format the book details
            return cls._format_book_details(data, olid)
        
        except requests.RequestException as e:
            logger.error(f"Error getting book details for {olid}: {str(e)}")
            return None

    @classmethod
    def _format_search_result(cls, doc):
        """
        Format a search result document from Open Library API
        """
        # Extract cover ID for cover image URL
        cover_id = doc.get('cover_i')
        cover_image = ""
        if cover_id:
            cover_image = f"{cls.COVERS_URL}/id/{cover_id}-M.jpg"
        
        # Extract authors
        authors = []
        if 'author_name' in doc:
            authors = doc['author_name']
        
        # Extract publication date
        published_date = None
        if 'first_publish_year' in doc:
            try:
                published_date = doc['first_publish_year']
            except (ValueError, TypeError):
                pass
        
        # Extract ISBN
        isbn = ""
        if 'isbn' in doc and doc['isbn']:
            isbn = doc['isbn'][0]
        
        # Extract languages
        languages = []
        if 'language' in doc:
            languages = doc['language']
        
        # Extract subjects and genres
        subjects = doc.get('subject', [])
        genres = []
        for subject in subjects:
            if any(genre_keyword in subject.lower() for genre_keyword in ['fiction', 'non-fiction', 'mystery', 'thriller', 'romance', 'sci-fi', 'fantasy', 'biography']):
                genres.append(subject)
        
        # Create a formatted result
        return {
            'olid': doc.get('key', '').replace('/works/', ''),
            'title': doc.get('title', ''),
            'authors': authors,
            'cover_image': cover_image,
            'isbn': isbn,
            'published_date': published_date,
            'languages': languages,
            'subjects': subjects[:10] if subjects else [],  # Limit to 10 subjects
            'genres': genres[:5] if genres else [],  # Limit to 5 genres
            'average_rating': None  # Open Library doesn't provide ratings
        }

    @classmethod
    def _format_book_details(cls, data, olid):
        """
        Format detailed book information from Open Library API
        """
        # Extract cover ID for cover image URL
        cover_id = data.get('covers', [None])[0] if 'covers' in data and data['covers'] else None
        cover_image = ""
        if cover_id:
            cover_image = f"{cls.COVERS_URL}/id/{cover_id}-L.jpg"
        
        # Extract authors
        authors = []
        if 'authors' in data:
            for author in data['authors']:
                if isinstance(author, dict) and 'name' in author:
                    authors.append(author['name'])
                elif isinstance(author, dict) and 'author' in author and 'key' in author['author']:
                    # Need to make another API call to get author name
                    author_key = author['author']['key']
                    try:
                        author_response = requests.get(f"{cls.BASE_URL}{author_key}.json")
                        if author_response.status_code == 200:
                            author_data = author_response.json()
                            if 'name' in author_data:
                                authors.append(author_data['name'])
                    except:
                        pass
        
        # Extract publication date
        published_date = None
        if 'publish_date' in data:
            try:
                # Try to parse the date in various formats
                date_formats = ["%Y", "%Y-%m-%d", "%B %Y", "%b %Y", "%d %B %Y", "%B %d, %Y"]
                for fmt in date_formats:
                    try:
                        published_date = datetime.strptime(data['publish_date'], fmt).strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
            except:
                published_date = data.get('publish_date')
        elif 'first_publish_date' in data:
            published_date = data.get('first_publish_date')
        
        # Extract ISBN
        isbn = ""
        if 'isbn_13' in data and data['isbn_13']:
            isbn = data['isbn_13'][0]
        elif 'isbn_10' in data and data['isbn_10']:
            isbn = data['isbn_10'][0]
        
        # Extract publisher
        publisher = ""
        if 'publishers' in data and data['publishers']:
            publisher = data['publishers'][0]
        
        # Extract page count
        page_count = None
        if 'number_of_pages' in data:
            try:
                page_count = int(data['number_of_pages'])
            except (ValueError, TypeError):
                pass
        
        # Extract language
        language = ""
        if 'languages' in data and data['languages']:
            lang_key = data['languages'][0]['key']
            language = lang_key.split('/')[-1]
        
        # Extract subjects and genres
        subjects = []
        if 'subjects' in data:
            subjects = data['subjects']
        
        genres = []
        for subject in subjects:
            if any(genre_keyword in subject.lower() for genre_keyword in ['fiction', 'non-fiction', 'mystery', 'thriller', 'romance', 'sci-fi', 'fantasy', 'biography']):
                genres.append(subject)
        
        # Create a formatted result
        return {
            'olid': olid,
            'title': data.get('title', ''),
            'subtitle': data.get('subtitle', ''),
            'authors': authors,
            'cover_image': cover_image,
            'isbn': isbn,
            'publisher': publisher,
            'published_date': published_date,
            'edition': data.get('edition_name', ''),
            'page_count': page_count,
            'language': language,
            'subjects': subjects[:20] if subjects else [],  # Limit to 20 subjects
            'genres': genres[:10] if genres else [],  # Limit to 10 genres
            'keywords': data.get('keywords', [])[:15] if 'keywords' in data else [],  # Limit to 15 keywords
            'mood_tags': [],  # Open Library doesn't provide mood tags
            'age_range': '',  # Open Library doesn't provide age range
            'author_countries': [],  # Open Library doesn't provide author countries
            'setting_country': '',  # Open Library doesn't provide setting country
            'average_rating': None,  # Open Library doesn't provide ratings
            'description': data.get('description', {}).get('value', '') if isinstance(data.get('description'), dict) else data.get('description', '')
        }

    @classmethod
    def save_book_to_db(cls, book_data):
        """
        Save book data to the database
        
        Parameters:
        - book_data: Dictionary containing book details
        
        Returns:
        - Book object
        """
        # Check if the book already exists by ISBN
        isbn = book_data.get('isbn', '')
        if isbn:
            existing_book = Book.objects.filter(isbn=isbn).first()
            if existing_book:
                return existing_book
        
        # Create a new book object
        book = Book(
            title=book_data.get('title', ''),
            subtitle=book_data.get('subtitle', ''),
            authors=book_data.get('authors', []),
            isbn=isbn,
            publisher=book_data.get('publisher', ''),
            published_date=book_data.get('published_date') if book_data.get('published_date') else None,
            edition=book_data.get('edition', ''),
            page_count=book_data.get('page_count'),
            language=book_data.get('language', ''),
            genres=book_data.get('genres', []),
            subjects=book_data.get('subjects', []),
            keywords=book_data.get('keywords', []),
            mood_tags=book_data.get('mood_tags', []),
            age_range=book_data.get('age_range', ''),
            author_countries=book_data.get('author_countries', []),
            setting_country=book_data.get('setting_country', ''),
            cover_image=book_data.get('cover_image', ''),
            average_rating=book_data.get('average_rating')
        )
        
        # Save the book to the database
        book.save()
        return book
