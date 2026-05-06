package com.gameleaderboard.partidas;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private GameSessionRepository gameSessionRepository;

    @Override
    public void run(String... args) throws Exception {
        // Verificar si ya hay datos
        if (gameSessionRepository.count() > 0) {
            System.out.println("Base de datos ya contiene datos. Omitiendo seed.");
            return;
        }

        System.out.println("Iniciando seed de 20,000 registros...");
        List<GameSession> sessions = new ArrayList<>();
        Random random = new Random();

        Long[] userIds = {1L, 2L, 3L, 4L, 5L, 6L, 7L, 8L, 9L, 10L};
        Long[] gameIds = {1L, 2L, 3L, 4L, 5L};
        String[] statuses = {"COMPLETED", "ABANDONED", "PAUSED"};
        String[] difficulties = {"EASY", "MEDIUM", "HARD"};

        for (int i = 0; i < 20000; i++) {
            GameSession session = new GameSession();
            session.setUserId(userIds[random.nextInt(userIds.length)]);
            session.setGameId(gameIds[random.nextInt(gameIds.length)]);
            session.setScore(random.nextInt(10000) + 100);
            session.setDurationSeconds((long) (random.nextInt(3600) + 60));
            
            LocalDateTime now = LocalDateTime.now();
            session.setStartTime(now.minusHours(random.nextInt(720))); // hasta 30 días atrás
            session.setEndTime(session.getStartTime().plusSeconds(session.getDurationSeconds()));
            
            session.setStatus(statuses[random.nextInt(statuses.length)]);
            session.setDifficulty(difficulties[random.nextInt(difficulties.length)]);
            session.setLevel(random.nextInt(100) + 1);
            session.setCreatedAt(session.getStartTime());

            sessions.add(session);

            // Guardar en lotes de 1000
            if ((i + 1) % 1000 == 0) {
                gameSessionRepository.saveAll(sessions);
                System.out.println("Guardados " + (i + 1) + " registros...");
                sessions.clear();
            }
        }

        // Guardar los últimos registros
        if (!sessions.isEmpty()) {
            gameSessionRepository.saveAll(sessions);
            System.out.println("Seed completado: 20,000 registros insertados.");
        }
    }
}
