package com.gameleaderboard.partidas;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/sessions")
@CrossOrigin(origins = "*")
public class GameSessionController {

    @Autowired
    private GameSessionRepository gameSessionRepository;

    @GetMapping
    public ResponseEntity<List<GameSession>> getAllSessions() {
        List<GameSession> sessions = gameSessionRepository.findAll();
        return ResponseEntity.ok(sessions);
    }

    @GetMapping("/{id}")
    public ResponseEntity<GameSession> getSessionById(@PathVariable Long id) {
        Optional<GameSession> session = gameSessionRepository.findById(id);
        return session.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<GameSession> createSession(@RequestBody GameSession session) {
        GameSession savedSession = gameSessionRepository.save(session);
        return ResponseEntity.ok(savedSession);
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<GameSession>> getSessionsByUser(@PathVariable Long userId) {
        List<GameSession> sessions = gameSessionRepository.findByUserIdOrderByEndTimeDesc(userId);
        return ResponseEntity.ok(sessions);
    }

    @GetMapping("/game/{gameId}")
    public ResponseEntity<List<GameSession>> getSessionsByGame(@PathVariable Long gameId) {
        List<GameSession> sessions = gameSessionRepository.findByGameIdOrderByScoreDesc(gameId);
        return ResponseEntity.ok(sessions);
    }

    @PutMapping("/{id}")
    public ResponseEntity<GameSession> updateSession(@PathVariable Long id, @RequestBody GameSession sessionDetails) {
        Optional<GameSession> session = gameSessionRepository.findById(id);
        if (session.isPresent()) {
            GameSession existing = session.get();
            if (sessionDetails.getScore() != null) existing.setScore(sessionDetails.getScore());
            if (sessionDetails.getStatus() != null) existing.setStatus(sessionDetails.getStatus());
            if (sessionDetails.getEndTime() != null) existing.setEndTime(sessionDetails.getEndTime());
            GameSession updated = gameSessionRepository.save(existing);
            return ResponseEntity.ok(updated);
        }
        return ResponseEntity.notFound().build();
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSession(@PathVariable Long id) {
        if (gameSessionRepository.existsById(id)) {
            gameSessionRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }
}
