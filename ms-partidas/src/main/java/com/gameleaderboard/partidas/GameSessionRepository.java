package com.gameleaderboard.partidas;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface GameSessionRepository extends JpaRepository<GameSession, Long> {

    List<GameSession> findByUserId(Long userId);

    List<GameSession> findByGameId(String gameId);

    List<GameSession> findByUserIdOrderByEndTimeDesc(Long userId);

    List<GameSession> findByGameIdOrderByScoreDesc(String gameId);

    Optional<GameSession> findById(Long id);

    @Query("SELECT g.userId, SUM(g.score) FROM GameSession g GROUP BY g.userId")
    List<Object[]> sumScoreByUser();
}
