import './ReviewButton.css';

interface Props {
  disabled: boolean;
  loading: boolean;
  onClick: () => void;
}

export function ReviewButton({ disabled, loading, onClick }: Props) {
  return (
    <button
      className="btn-primary"
      id="reviewBtn"
      disabled={disabled || loading}
      onClick={onClick}
    >
      {loading && <span className="spinner" />}
      <span>{loading ? 'Reviewing...' : '🔍 Review SRS'}</span>
    </button>
  );
}
