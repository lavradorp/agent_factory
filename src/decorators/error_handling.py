from functools import wraps

def error_handling():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
           
            instance = args[0] if args else None

            strategy_name = instance.__class__.__name__
            
            try:
                return func(*args, **kwargs)
            
            except ModuleNotFoundError as e:
                missing_package = e.name
                
                raise RuntimeError(
                    f"\n The strategy '{strategy_name}' needs an additional package.\n"
                    f" Run: uv add {missing_package}"
                ) from e
            
            except (ValueError, TypeError) as e:
                err_msg = str(e).lower()

                if "api_key" in err_msg or "did not find" in err_msg or "credential" in err_msg:
                    raise ValueError(
                        f"\nAuthetication failure on '{strategy_name} strategy'.\n"
                    ) from e
                raise e
            
            except Exception as e:
                raise RuntimeError(f"\nFailure on '{strategy_name}': {str(e)}") from e
            
        return wrapper
    
    return decorator

