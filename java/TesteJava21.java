import java.util.concurrent.CountDownLatch;
import java.util.concurrent.Executors;

/**
 * Exemplo simples em Java 21 usando Virtual Threads para simular 10.000 tarefas paralelas.
 * Cada tarefa imprime seu ID e simula um trabalho com Thread.sleep.
 * Usa ExecutorService com Virtual Threads para eficiência.
 */
public class TesteJava21 {

    public static void main(String[] args) throws InterruptedException {
        // Latch para esperar todas as tarefas terminarem
        CountDownLatch latch = new CountDownLatch(10000);

        // Executor com Virtual Threads (Java 21+)
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            for (int i = 0; i < 10000; i++) {
                int taskId = i;
                executor.submit(() -> {
                    try {
                        // Simula trabalho: imprime "Olá mundo" e dorme por 100ms
                        System.out.println("Olá mundo from Task " + taskId + " on " + Thread.currentThread().getName());
                        Thread.sleep(100); // Simulação de tarefa
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        latch.countDown(); // Decrementa o latch
                    }
                });
            }
        }

        // Espera todas as tarefas terminarem
        latch.await();
        System.out.println("Todas as 10.000 tarefas concluídas!");
    }
}