import logging
import sys

from src.config.logger import Logger
from src.extractors import download_reports
from src.loaders import insert_beach_status
from src.transformers import structuring_data
from src.utils import remove_pdfs

class BeachEtlPipeline:
    def __init__(self):
        self.logger = Logger().get_logger(__name__)

    def run(self):
        self.logger.warning('Starting BeachEtlPipeline')

        try:
            # Extract
            reports_info = download_reports()
            self.logger.warning(f"Downloaded {len(reports_info)} reports")

            # Transform and Load
            for i in reports_info:
                structured_data = structuring_data(i['fileDownloadPath'], i['dateRef'], i['slug'])
                insert_beach_status(structured_data, i['dateRefFormatted'])
                self.logger.warning(f"Processed report for {i['slug']} dated {i['dateRefFormatted']}")

            # Cleanup
            remove_pdfs()
            self.logger.warning("Removed temporary PDF files")

            self.logger.warning('Finished BeachEtlPipeline')


        except Exception as e:
            self.logger.warning(f"An error occurred in pipeline: {e}", exc_info=True)


if __name__ == "__main__":
    pipeline = BeachEtlPipeline()
    pipeline.run()
