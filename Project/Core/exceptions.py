class ProductNotFoundException(Exception):
    """Erro levantado quando o produto não é encontrado no site."""
    pass

class FileNotFoundException(Exception):
    """Erro levantado quando o arquivo .xlsx não existe."""
    pass

class ScraperException(Exception):
    """Erro geral do scraper."""
    pass
