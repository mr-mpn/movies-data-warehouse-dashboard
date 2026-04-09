import { useState, useEffect } from 'react'
import './Home.css'

const API_URL = import.meta.env.VITE_API_URL

const FIELD_LABELS = {
  title: 'Title',
  overview: 'Overview',
  release_date: 'Release Date',
  spoken_languages_names: 'Languages',
}

function Home({ user, onLoginClick, onLogout }) {
  const [movies, setMovies] = useState([])
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(10)
  const [totalPages, setTotalPages] = useState(1)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedMovie, setSelectedMovie] = useState(null)
  const [modalLoading, setModalLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetch(`${API_URL}/home?page=${page}&page_size=${pageSize}`)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch movies')
        return res.json()
      })
      .then(data => {
        setMovies(data.movies)
        setTotalPages(data.total_pages)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [page, pageSize])

  const handlePageSizeChange = (e) => {
    setPageSize(Number(e.target.value))
    setPage(1)
  }

  const handleMovieClick = async (movieId) => {
    setModalLoading(true)
    setSelectedMovie(null)
    try {
      const res = await fetch(`${API_URL}/movie?movie_id=${movieId}`)
      if (!res.ok) throw new Error('Movie not found')
      const data = await res.json()
      setSelectedMovie(data)
    } catch {
      setSelectedMovie(null)
    } finally {
      setModalLoading(false)
    }
  }

  const closeModal = () => {
    setSelectedMovie(null)
    setModalLoading(false)
  }

  const getPageNumbers = () => {
    const pages = []
    const maxVisible = 5
    let start = Math.max(1, page - Math.floor(maxVisible / 2))
    let end = Math.min(totalPages, start + maxVisible - 1)
    start = Math.max(1, end - maxVisible + 1)

    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    return pages
  }

  return (
    <>
      <nav className="navbar">
        <div className="navbar-brand">MoviesDash</div>
        <div className="navbar-actions">
          {user ? (
            <>
              <span>{user}</span>
              <button className="btn-signout" onClick={onLogout}>Sign Out</button>
            </>
          ) : (
            <button className="btn-signin" onClick={onLoginClick}>Sign In</button>
          )}
        </div>
      </nav>

      <div className="hero-banner">
        <h1>Top Voted Movies</h1>
        <p>Check out the highest rated films from our collection</p>
      </div>

      <div className="home-content">
        <div className="section-header">
          <h2>Top Rated</h2>
          <select value={pageSize} onChange={handlePageSizeChange}>
            <option value={10}>10 per page</option>
            <option value={15}>15 per page</option>
            <option value={20}>20 per page</option>
          </select>
        </div>

        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error">{error}</div>}

        {!loading && !error && (
          <>
            <div className="movies-grid">
              {movies.map((movie, index) => (
                <div className="movie-card" key={index}>
                  <div className="movie-rank">#{(page - 1) * pageSize + index + 1}</div>
                  <div
                    className="movie-title clickable"
                    onClick={() => handleMovieClick(movie.id)}
                  >
                    {movie.title}
                  </div>
                  <div className="movie-stats">
                    <div className="movie-rating">
                      <span className="star">*</span> {movie.vote_average.toFixed(1)}
                    </div>
                    <div className="movie-votes">
                      {Math.round(movie.vote_count).toLocaleString()} votes
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="pagination">
              <button
                onClick={() => setPage(p => p - 1)}
                disabled={page === 1}
              >
                Previous
              </button>

              {getPageNumbers().map(num => (
                <button
                  key={num}
                  className={num === page ? 'page-num active' : 'page-num'}
                  onClick={() => setPage(num)}
                >
                  {num}
                </button>
              ))}

              <button
                onClick={() => setPage(p => p + 1)}
                disabled={page === totalPages}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>

      {(selectedMovie || modalLoading) && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            {modalLoading ? (
              <div className="modal-loading">Loading...</div>
            ) : (
              <>
                <button className="modal-close" onClick={closeModal}>X</button>
                <div className="modal-fields">
                  {Object.entries(FIELD_LABELS).map(([key, label]) =>
                    selectedMovie[key] ? (
                      <div className="modal-field" key={key}>
                        <div className="modal-label">{label}</div>
                        <div className="modal-value">{selectedMovie[key]}</div>
                      </div>
                    ) : null
                  )}
                  {selectedMovie.imdb_id && (
                    <div className="modal-field">
                      <a
                        className="imdb-link"
                        href={`https://www.imdb.com/title/${selectedMovie.imdb_id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        title="View on IMDb"
                      >
                        IMDb
                      </a>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </>
  )
}

export default Home
