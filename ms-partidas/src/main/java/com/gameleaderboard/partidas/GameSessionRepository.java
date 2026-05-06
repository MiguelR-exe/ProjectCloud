package com.gameleaderboard.partidas;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface GameSessionRepository extends JpaRepository<GameSession, Long> {

    List<GameSession> findByUserId(Long userId);

    List<GameSession> findByGameId(Long gameId);

    List<GameSession> findByUserIdOrderByEndTimeDesc(Long userId);

    List<GameSession> findByGameIdOrderByScoreDesc(Long gameId);

    Optional<GameSession> findById(Long id);
}
