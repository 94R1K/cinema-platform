from abc import ABC, abstractmethod


class BaseElasticTransformer[T, R](ABC):
    @abstractmethod
    def transform(self, item: T) -> R:
        raise NotImplementedError
    
    def transform_batch(self, items: list[T]) -> list[R]:
        return [self.transform(item) for item in items]
