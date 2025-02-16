"""
Starter for demonstration of laboratory work.
"""
# pylint: disable= too-many-locals, undefined-variable, unused-import
from pathlib import Path

from config.constants import PROJECT_ROOT
from config.lab_settings import LabSettings
from lab_7_llm.main import (
    LLMPipeline,
    RawDataImporter,
    RawDataPreprocessor,
    report_time,
    TaskDataset,
    TaskEvaluator,
)


@report_time
def main() -> None:
    """
    Run the translation pipeline.
    """
    settings = LabSettings(PROJECT_ROOT/'lab_7_llm'/'settings.json')

    importer = RawDataImporter(settings.parameters.dataset)
    importer.obtain()

    if importer.raw_data is None:
        return

    preprocessor = RawDataPreprocessor(importer.raw_data)
    preprocessor.transform()

    dataset = TaskDataset(preprocessor.data.head(100))

    pipeline = LLMPipeline(settings.parameters.model,
                           dataset,
                           max_length=120,
                           batch_size=64,
                           device="cpu")
    data_frame = pipeline.infer_dataset()

    predictions_path = PROJECT_ROOT / "lab_7_llm" / "dist" / "predictions.csv"
    predictions_path.parent.mkdir(exist_ok=True)
    data_frame.to_csv(predictions_path)

    evaluator = TaskEvaluator(predictions_path, settings.parameters.metrics)

    print(evaluator.run())

    result = evaluator.run()
    assert result is not None, "Demo does not work correctly"


if __name__ == "__main__":
    main()
