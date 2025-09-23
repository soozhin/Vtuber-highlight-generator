import { useState } from "react";
import "./App.css";

function App() {
	const [youtubeUrl, setYoutubeUrl] = useState("");
	const [clips, setClips] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	const fetchHighlights = async () => {
		if (!youtubeUrl) return;

		setLoading(true);
		setError("");
		setClips([]);

		try {
			const res = await fetch(
				"http://localhost:8000/api/v1/generate-highlight",
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ url: youtubeUrl }),
				}
			);

			if (!res.ok) throw new Error("Failed to fetch highlights");

			const data = await res.json();
			setClips(data.download_links || []);
		} catch (err) {
			console.error(err);
			setError("Error fetching highlights");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
			<h1>Vtuber Highlight Search</h1>
			<input
				type="text"
				placeholder="Enter YouTube URL"
				value={youtubeUrl}
				onChange={(e) => setYoutubeUrl(e.target.value)}
				style={{ width: "70%", padding: "8px", marginRight: "10px" }}
				onKeyUp={(e) => e.key === "Enter" && fetchHighlights()}
			/>
			<button onClick={fetchHighlights} style={{ padding: "8px 12px" }}>
				Search
			</button>

			{loading && <p>Loading...</p>}
			{error && <p style={{ color: "red" }}>{error}</p>}

			<div style={{ marginTop: "20px" }}>
				{clips.map((clip, index) => (
					<div key={index} style={{ marginBottom: "15px" }}>
						<video src={clip} controls width="400" />
					</div>
				))}
			</div>
		</div>
	);
}

export default App;
