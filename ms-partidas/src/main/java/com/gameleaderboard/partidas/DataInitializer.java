package com.gameleaderboard.partidas;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

@Component
public class DataInitializer implements CommandLineRunner {

    @Autowired
    private GameSessionRepository gameSessionRepository;

    @Override
    public void run(String... args) throws Exception {
        if (gameSessionRepository.count() > 0) {
            System.out.println("Base de datos ya contiene datos. Omitiendo seed.");
            return;
        }

        String[] gameIds = fetchGameIds();

        int totalSessions = 800000;
        int totalUsers    = 20000;
        System.out.println("Iniciando seed de " + totalSessions + " registros con " + gameIds.length + " juegos...");

        List<GameSession> sessions = new ArrayList<>();
        Random random = new Random();
        String[] statuses    = {"COMPLETED", "ABANDONED", "PAUSED"};
        String[] difficulties = {"EASY", "MEDIUM", "HARD"};

        for (int i = 0; i < totalSessions; i++) {
            GameSession session = new GameSession();
            session.setUserId((long)(random.nextInt(totalUsers) + 1));
            session.setGameId(gameIds[random.nextInt(gameIds.length)]);
            session.setScore(random.nextInt(10000) + 100);
            session.setDurationSeconds((long)(random.nextInt(3600) + 60));

            LocalDateTime start = LocalDateTime.now().minusHours(random.nextInt(720));
            session.setStartTime(start);
            session.setEndTime(start.plusSeconds(session.getDurationSeconds()));
            session.setStatus(statuses[random.nextInt(statuses.length)]);
            session.setDifficulty(difficulties[random.nextInt(difficulties.length)]);
            session.setLevel(random.nextInt(100) + 1);
            session.setCreatedAt(start);

            sessions.add(session);

            if ((i + 1) % 5000 == 0) {
                gameSessionRepository.saveAll(sessions);
                System.out.println("Guardados " + (i + 1) + " registros...");
                sessions.clear();
            }
        }

        if (!sessions.isEmpty()) gameSessionRepository.saveAll(sessions);
        System.out.println("Seed completado: " + totalSessions + " registros insertados.");
    }

    @SuppressWarnings("unchecked")
    private String[] fetchGameIds() {
        String msJuegosUrl = System.getenv().getOrDefault("MS_JUEGOS_URL", "http://ms-juegos:8002");
        RestTemplate restTemplate = new RestTemplate();

        for (int attempt = 0; attempt < 10; attempt++) {
            try {
                List<Map<String, Object>> games = restTemplate.exchange(
                    msJuegosUrl + "/api/games?page=1&limit=100",
                    HttpMethod.GET, null,
                    new ParameterizedTypeReference<List<Map<String, Object>>>() {}
                ).getBody();

                if (games != null && !games.isEmpty()) {
                    return games.stream()
                        .map(g -> (String) g.get("_id"))
                        .filter(id -> id != null)
                        .toArray(String[]::new);
                }
            } catch (Exception e) {
                System.out.println("Esperando ms-juegos... intento " + (attempt + 1) + "/10");
                try { Thread.sleep(4000); } catch (InterruptedException ignored) {}
            }
        }

        System.out.println("No se pudo conectar a ms-juegos. Usando IDs de fallback.");
        return new String[]{"fallback-1", "fallback-2", "fallback-3"};
    }
}
