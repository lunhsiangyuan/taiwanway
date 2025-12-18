"""
記憶系統工具
提供短期和長期記憶功能，讓 Subagent 能夠記住分析結果和上下文。

記憶類型：
- 短期記憶：會話內有效，容量有限（FIFO）
- 長期記憶：持久化存儲，支援過期機制
- 情節記憶：完整分析事件的記錄
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from collections import deque
import json
import hashlib
import logging
import os

logger = logging.getLogger(__name__)

# 預設存儲路徑
DEFAULT_STORAGE_PATH = "agents/memory_store"
SHORT_TERM_CAPACITY = 100


@dataclass
class MemoryEntry:
    """記憶項目"""
    key: str
    value: Any
    memory_type: str  # "short_term", "long_term", "episodic"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    accessed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    access_count: int = 0
    ttl: Optional[int] = None  # Time to live in seconds
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_expired(self) -> bool:
        """檢查記憶是否過期"""
        if self.ttl is None:
            return False
        created = datetime.fromisoformat(self.created_at)
        return datetime.now() > created + timedelta(seconds=self.ttl)

    def touch(self):
        """更新訪問時間和計數"""
        self.accessed_at = datetime.now().isoformat()
        self.access_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return {
            "key": self.key,
            "value": self.value if not callable(self.value) else str(self.value),
            "memory_type": self.memory_type,
            "created_at": self.created_at,
            "accessed_at": self.accessed_at,
            "access_count": self.access_count,
            "ttl": self.ttl,
            "tags": self.tags,
            "metadata": self.metadata
        }


class MemoryStore:
    """
    整合的記憶存儲系統
    """
    _instance = None
    _short_term: deque = None
    _long_term: Dict[str, MemoryEntry] = None
    _episodes: List[Dict[str, Any]] = None
    _storage_path: Path = None

    def __new__(cls, storage_path: str = DEFAULT_STORAGE_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(storage_path)
        return cls._instance

    def _initialize(self, storage_path: str):
        """初始化記憶存儲"""
        self._storage_path = Path(storage_path)
        self._storage_path.mkdir(parents=True, exist_ok=True)

        self._short_term = deque(maxlen=SHORT_TERM_CAPACITY)
        self._long_term = {}
        self._episodes = []

        # 載入長期記憶索引
        self._load_long_term_index()
        self._load_episodes()

        logger.info(f"記憶系統初始化完成，存儲路徑：{self._storage_path}")

    def _load_long_term_index(self):
        """載入長期記憶索引"""
        index_file = self._storage_path / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                    for key, meta in index_data.items():
                        self._long_term[key] = MemoryEntry(
                            key=key,
                            value=None,  # 延遲載入
                            memory_type="long_term",
                            created_at=meta.get("created_at", datetime.now().isoformat()),
                            tags=meta.get("tags", []),
                            ttl=meta.get("ttl")
                        )
                logger.info(f"載入 {len(self._long_term)} 個長期記憶項目")
            except Exception as e:
                logger.error(f"載入長期記憶索引失敗：{str(e)}")

    def _save_long_term_index(self):
        """保存長期記憶索引"""
        index_data = {
            key: {
                "created_at": entry.created_at,
                "tags": entry.tags,
                "ttl": entry.ttl,
                "access_count": entry.access_count
            }
            for key, entry in self._long_term.items()
        }
        index_file = self._storage_path / "index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)

    def _get_file_path(self, key: str) -> Path:
        """取得記憶檔案路徑"""
        safe_key = hashlib.md5(key.encode()).hexdigest()[:16]
        return self._storage_path / f"{safe_key}.json"

    def _load_episodes(self):
        """載入情節記憶"""
        episodes_dir = self._storage_path / "episodes"
        if episodes_dir.exists():
            for file in episodes_dir.glob("episode_*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        self._episodes.append(json.load(f))
                except Exception as e:
                    logger.error(f"載入情節失敗：{file}, {str(e)}")
            self._episodes.sort(key=lambda x: x.get("timestamp", ""))


# 全局記憶存儲實例
_memory_store: Optional[MemoryStore] = None


def _get_store() -> MemoryStore:
    """獲取記憶存儲實例"""
    global _memory_store
    if _memory_store is None:
        _memory_store = MemoryStore()
    return _memory_store


def remember(
    key: str,
    value: Any,
    persist: bool = False,
    tags: Optional[List[str]] = None,
    ttl: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    記住某事

    參數:
        key: 記憶鍵
        value: 記憶值
        persist: 是否持久化（長期記憶）
        tags: 標籤列表
        ttl: 過期時間（秒）
        metadata: 額外元數據

    返回:
        操作結果
    """
    store = _get_store()
    tags = tags or []
    metadata = metadata or {}

    try:
        entry = MemoryEntry(
            key=key,
            value=value,
            memory_type="long_term" if persist else "short_term",
            tags=tags,
            ttl=ttl,
            metadata=metadata
        )

        # 存入短期記憶
        store._short_term.append(entry)

        # 如果需要持久化
        if persist:
            # 寫入檔案
            file_path = store._get_file_path(key)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(entry.to_dict(), f, ensure_ascii=False, indent=2, default=str)

            # 更新索引
            store._long_term[key] = entry
            store._save_long_term_index()

        logger.info(f"記憶已存儲: {key} (persist={persist})")

        return {
            "status": "success",
            "key": key,
            "persist": persist,
            "tags": tags
        }

    except Exception as e:
        logger.error(f"記憶存儲失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def recall(
    key: str,
    check_long_term: bool = True
) -> Dict[str, Any]:
    """
    回憶某事

    參數:
        key: 記憶鍵
        check_long_term: 是否檢查長期記憶

    返回:
        記憶值或 None
    """
    store = _get_store()

    try:
        # 先查短期記憶
        for entry in store._short_term:
            if entry.key == key:
                entry.touch()
                return {
                    "status": "success",
                    "key": key,
                    "value": entry.value,
                    "memory_type": "short_term",
                    "access_count": entry.access_count
                }

        # 再查長期記憶
        if check_long_term and key in store._long_term:
            entry = store._long_term[key]

            # 檢查是否過期
            if entry.is_expired():
                forget(key)
                return {
                    "status": "expired",
                    "key": key,
                    "message": "記憶已過期"
                }

            # 延遲載入值
            if entry.value is None:
                file_path = store._get_file_path(key)
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        entry.value = data.get("value")

            entry.touch()

            # 載入到短期記憶加速後續訪問
            store._short_term.append(entry)

            return {
                "status": "success",
                "key": key,
                "value": entry.value,
                "memory_type": "long_term",
                "access_count": entry.access_count
            }

        return {
            "status": "not_found",
            "key": key,
            "message": "記憶不存在"
        }

    except Exception as e:
        logger.error(f"記憶回憶失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def forget(key: str) -> Dict[str, Any]:
    """
    忘記某事（刪除記憶）

    參數:
        key: 記憶鍵

    返回:
        操作結果
    """
    store = _get_store()

    try:
        deleted = False

        # 從短期記憶刪除
        store._short_term = deque(
            [e for e in store._short_term if e.key != key],
            maxlen=SHORT_TERM_CAPACITY
        )

        # 從長期記憶刪除
        if key in store._long_term:
            del store._long_term[key]
            file_path = store._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
            store._save_long_term_index()
            deleted = True

        return {
            "status": "success" if deleted else "not_found",
            "key": key,
            "deleted": deleted
        }

    except Exception as e:
        logger.error(f"刪除記憶失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def search_by_tag(tag: str) -> Dict[str, Any]:
    """
    按標籤搜索記憶

    參數:
        tag: 標籤

    返回:
        匹配的記憶列表
    """
    store = _get_store()

    try:
        results = []

        # 搜索短期記憶
        for entry in store._short_term:
            if tag in entry.tags:
                results.append({
                    "key": entry.key,
                    "memory_type": "short_term",
                    "created_at": entry.created_at,
                    "tags": entry.tags
                })

        # 搜索長期記憶
        for key, entry in store._long_term.items():
            if tag in entry.tags and not entry.is_expired():
                results.append({
                    "key": key,
                    "memory_type": "long_term",
                    "created_at": entry.created_at,
                    "tags": entry.tags
                })

        return {
            "status": "success",
            "tag": tag,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        logger.error(f"標籤搜索失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def record_analysis(
    analysis_type: str,
    context: Dict[str, Any],
    results: Dict[str, Any],
    insights: List[str],
    lessons: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    記錄一次分析（情節記憶）

    參數:
        analysis_type: 分析類型（如 "sales_analysis", "customer_segmentation"）
        context: 上下文信息
        results: 分析結果
        insights: 洞察
        lessons: 學到的經驗

    返回:
        情節 ID
    """
    store = _get_store()

    try:
        episode_id = f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        episode = {
            "episode_id": episode_id,
            "episode_type": analysis_type,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "results": results,
            "insights": insights,
            "lessons": lessons or [],
            "success": results.get("status") == "success"
        }

        # 保存到檔案
        episodes_dir = store._storage_path / "episodes"
        episodes_dir.mkdir(parents=True, exist_ok=True)

        file_path = episodes_dir / f"episode_{episode_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(episode, f, ensure_ascii=False, indent=2, default=str)

        store._episodes.append(episode)

        logger.info(f"情節已記錄: {episode_id}")

        return {
            "status": "success",
            "episode_id": episode_id,
            "analysis_type": analysis_type
        }

    except Exception as e:
        logger.error(f"記錄情節失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def get_experience(
    analysis_type: str,
    limit: int = 5
) -> Dict[str, Any]:
    """
    取得相關的過往經驗

    參數:
        analysis_type: 分析類型
        limit: 返回數量限制

    返回:
        相關情節列表
    """
    store = _get_store()

    try:
        matching = [
            ep for ep in store._episodes
            if ep.get("episode_type") == analysis_type
        ]

        # 按時間倒序，返回最近的
        matching.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        matching = matching[:limit]

        # 提取經驗教訓
        all_lessons = []
        for ep in matching:
            all_lessons.extend(ep.get("lessons", []))

        return {
            "status": "success",
            "analysis_type": analysis_type,
            "count": len(matching),
            "experiences": matching,
            "lessons_learned": list(set(all_lessons))
        }

    except Exception as e:
        logger.error(f"獲取經驗失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def clear_memory(memory_type: str = "short_term") -> Dict[str, Any]:
    """
    清空記憶

    參數:
        memory_type: 記憶類型（"short_term", "long_term", "all"）

    返回:
        操作結果
    """
    store = _get_store()

    try:
        cleared = {"short_term": 0, "long_term": 0}

        if memory_type in ["short_term", "all"]:
            cleared["short_term"] = len(store._short_term)
            store._short_term.clear()

        if memory_type in ["long_term", "all"]:
            cleared["long_term"] = len(store._long_term)
            for key in list(store._long_term.keys()):
                file_path = store._get_file_path(key)
                if file_path.exists():
                    file_path.unlink()
            store._long_term.clear()
            store._save_long_term_index()

        logger.info(f"記憶已清空: {cleared}")

        return {
            "status": "success",
            "cleared": cleared
        }

    except Exception as e:
        logger.error(f"清空記憶失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


def get_memory_summary() -> Dict[str, Any]:
    """
    取得記憶系統摘要

    返回:
        記憶系統統計
    """
    store = _get_store()

    try:
        # 收集所有標籤
        all_tags = set()
        for entry in store._short_term:
            all_tags.update(entry.tags)
        for entry in store._long_term.values():
            all_tags.update(entry.tags)

        return {
            "status": "success",
            "short_term": {
                "count": len(store._short_term),
                "capacity": SHORT_TERM_CAPACITY
            },
            "long_term": {
                "count": len(store._long_term),
                "storage_path": str(store._storage_path)
            },
            "episodes": {
                "count": len(store._episodes)
            },
            "all_tags": list(all_tags)
        }

    except Exception as e:
        logger.error(f"獲取記憶摘要失敗：{str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
