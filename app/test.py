import asyncio

from latex.main import test_latex_flow, test_word_flow

asyncio.run(test_latex_flow()) # Works!
asyncio.run(test_word_flow()) # To Test!
