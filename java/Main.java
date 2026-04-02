/**
 * Exemplo em Java 21: Record para Produto e Switch Expression para descrição.
 */
record Produto(int id, String nome) {

    /**
     * Retorna uma descrição baseada no ID usando Switch Expression.
     */
    public String descricao() {
        return switch (id) {
            case 1 -> "Produto básico: " + nome;
            case 2 -> "Produto premium: " + nome;
            case 3 -> "Produto deluxe: " + nome;
            case 5 -> "Produto especial: " + nome;
            default -> "Produto desconhecido: " + nome;
        };
    }
}

public class Main {
    public static void main(String[] args) {
        Produto p1 = new Produto(1, "Caneta");
        Produto p2 = new Produto(2, "Notebook");
        Produto p3 = new Produto(3, "Smartphone");
        Produto p4 = new Produto(4, "Outro");
        Produto p5 = new Produto(5, "Relógio");

        System.out.println(p1.descricao()); // Produto básico: Caneta
        System.out.println(p2.descricao()); // Produto premium: Notebook
        System.out.println(p3.descricao()); // Produto deluxe: Smartphone
        System.out.println(p4.descricao()); // Produto desconhecido: Outro
        System.out.println(p5.descricao()); // Produto especial: Relógio
    }
}
