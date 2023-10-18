
from app.latex.models.compile_variable_info import ImageVariableInfo


class InlineLatexImage():
    """
    Class to generate an inline latex image
    """

    def __init__(self, info: ImageVariableInfo, path: str):
        self.info = info
        self.path = path

    def _insert_image(self):
        options = []
        if self.info.height is not None:
            options.append(f"height={self.info.height}mm")
        if self.info.width is not None:
            options.append(f"width={self.info.width}mm")
        
        return "\\includegraphics[%s]{%s}" % (','.join(options), self.path) 

    def __unicode__(self):
        return self._insert_image()

    def __str__(self):
        return self._insert_image()

    def __html__(self):
        return self._insert_image()