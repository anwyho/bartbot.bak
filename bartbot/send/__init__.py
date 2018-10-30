import logging

# TODO: Where should this function go....?


def set_if_exists(self,
                  valName,
                  val,
                  maxLen: int = -1,
                  types: list = [],
                  prefix: str = "",
                  raiseOnFail: bool = False):
    if val is not None:  # TODO make this more elegant
        # Max length provided
        if maxLen >= 0 and len(val) > maxLen:
            val = val[:maxLen]
            logging.warning(
                f"Attempted to set variable {valName} with length larger than the max length allowed ({maxLen} chars)." +
                (f" {valName} has been truncated to {val}." if not raiseOnFail else ""))
            if raiseOnFail:
                raise ValueError(
                    f"Value '{valName}' has too many characters. (Max allowed: {maxLen} chars)")
        # List of types provided
        elif types and val.lower() not in types:
            raise ValueError(
                f"{type(self).__name__} cannot take value {val.lower()} as {valName}. It does not match any of the types provided.")
        elif prefix is not "" and not val.startswith(prefix):
            raise ValueError(
                f"Expected value '{val}' to start with prefix {prefix}."
            )
        setattr(self, valName, val)
    elif raiseOnFail:
        raise ValueError(
            f"Given value '{val}' is None and raiseOnFail is True.")
