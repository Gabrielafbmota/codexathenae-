from enum import StrEnum


class ReadingStatus(StrEnum):
    WANT_TO_READ = "want_to_read"
    READING = "reading"
    READ = "read"
    ABANDONED = "abandoned"

    def can_transition_to(self, target: "ReadingStatus") -> bool:
        allowed: dict[ReadingStatus, set[ReadingStatus]] = {
            ReadingStatus.WANT_TO_READ: {ReadingStatus.READING},
            ReadingStatus.READING: {ReadingStatus.READ, ReadingStatus.ABANDONED},
            ReadingStatus.READ: {ReadingStatus.READING},
            ReadingStatus.ABANDONED: {ReadingStatus.READING},
        }
        return target in allowed.get(self, set())
