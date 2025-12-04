// src/pages/UpcomingIPOs.jsx
import React, { useEffect, useState } from 'react';

function UpcomingIPOs() {
  const [ipos, setIpos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [q, setQ] = useState('');
  const [error, setError] = useState(null);

  async function fetchIPOs() {
    setLoading(true);
    try {
      const res = await fetch('/api/ipos/upcoming/');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setIpos(data.results || data); // handle pagination
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchIPOs();
  }, []);

  const filtered = ipos.filter(i =>
    (i.title || '').toLowerCase().includes(q.toLowerCase()) ||
    (i.company?.name || '').toLowerCase().includes(q.toLowerCase())
  );

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Upcoming IPOs</h1>
      <input
        placeholder="Search by company or title..."
        value={q}
        onChange={e => setQ(e.target.value)}
        className="w-full p-2 mb-4 border rounded"
      />
      {loading && <div>Loading...</div>}
      {error && <div className="text-red-600">Error: {error}</div>}
      <div className="space-y-4">
        {filtered.map(ipo => (
          <div key={ipo.id} className="p-4 border rounded shadow-sm">
            <div className="flex justify-between">
              <div>
                <h2 className="text-lg font-semibold">{ipo.title}</h2>
                <div className="text-sm text-gray-600">{ipo.company?.name} • {ipo.exchange}</div>
                <p className="mt-2">{ipo.short_description}</p>
              </div>
              <div className="text-right">
                <div>Issue: {ipo.issue_start_date} → {ipo.issue_end_date}</div>
                <div className="mt-2">Price band: {ipo.price_band_min} - {ipo.price_band_max}</div>
                <div className="mt-2">Lot: {ipo.lot_size}</div>
              </div>
            </div>
            <div className="mt-3 flex gap-2">
              <a href={`/ipo/${ipo.id}`} className="underline">Details</a>
              <a href={ipo.documents?.[0]?.file_url} target="_blank" rel="noreferrer">RHP</a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UpcomingIPOs;
