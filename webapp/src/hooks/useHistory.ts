import { useState, useCallback } from 'react';
import type { HistoryEntry } from '../types/review';
import { STORAGE_KEY, MAX_HISTORY } from '../utils/constants';

function loadHistory(): HistoryEntry[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  } catch {
    return [];
  }
}

/**
 * React hook for managing review history in localStorage.
 */
export function useHistory() {
  const [history, setHistory] = useState<HistoryEntry[]>(loadHistory);

  const addEntry = useCallback((entry: HistoryEntry) => {
    setHistory(prev => {
      const updated = [entry, ...prev].slice(0, MAX_HISTORY);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const getEntry = useCallback((index: number): HistoryEntry | undefined => {
    return history[index];
  }, [history]);

  return { history, addEntry, getEntry };
}
