package org.neural;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.function.UnaryOperator;

public class Main {
    public static void main(String[] args) throws IOException {
        //dots();
        digits();
    }

    private static void dots() {
        FormDots f = new FormDots();
        new Thread(f).start();
    }

    private static void digits() throws  IOException {
        // Активационная функция и её производная
        UnaryOperator<Double> sigmoid = x -> 1 / (1 + Math.exp(-x));
        UnaryOperator<Double> dsigmoid = y -> y * (1 - y);

        // Создаём нейросеть: 784 (28x28) → 512 → 128 → 32 → 10 (цифры 0-9)
        NeuralNetwork neuralNetwork = new NeuralNetwork(0.001, sigmoid, dsigmoid, 784, 512, 128, 32, 10);

        // Получаем доступ к ресурсам через ClassLoader
        ClassLoader classLoader = Main.class.getClassLoader();
        java.net.URL directoryUrl = classLoader.getResource("train/trainingSample");

        if (directoryUrl == null) {
            throw new IOException("Directory not found in resources: train/trainingSample");
        }

        File trainingSampleDir;
        try {
            trainingSampleDir = new File(directoryUrl.toURI());
        } catch (Exception e) {
            throw new IOException("Failed to convert URL to file: " + directoryUrl, e);
        }

        if (!trainingSampleDir.exists()) {
            throw new IOException("Directory does not exist: " + trainingSampleDir.getAbsolutePath());
        }

        if (!trainingSampleDir.isDirectory()) {
            throw new IOException("Path is not a directory: " + trainingSampleDir.getAbsolutePath());
        }

        // Фильтруем только изображения
        File[] imagesFiles = trainingSampleDir.listFiles((dir, name) ->
                name.toLowerCase().endsWith(".png") ||
                        name.toLowerCase().endsWith(".jpg") ||
                        name.toLowerCase().endsWith(".jpeg")
        );

        if (imagesFiles == null || imagesFiles.length == 0) {
            throw new IOException("No image files found in: train/trainingSample");
        }

        int samples = imagesFiles.length;
        BufferedImage[] images = new BufferedImage[samples];
        int[] digits = new int[samples];

        // Загружаем изображения и метки
        for (int i = 0; i < samples; i++) {
            images[i] = ImageIO.read(imagesFiles[i]);

            // Извлечение цифры из имени файла (например: img_5_001.jpg → 5)
            String fileName = imagesFiles[i].getName();
            String fileNameWithoutExt = fileName.replaceAll("\\.(png|jpg|jpeg)$", ""); // убираем расширение
            String[] parts = fileNameWithoutExt.split("_");

            if (parts.length < 2) {
                throw new IOException("Invalid filename format: " + fileName + " (expected: name_digit_*.ext)");
            }

            try {
                digits[i] = Integer.parseInt(parts[1]); // цифра — второй элемент после split("_")
            } catch (NumberFormatException e) {
                throw new IOException("Cannot parse digit from filename: " + fileName, e);
            }
        }

        double[][] inputs = new double[samples][784];
        for (int i = 0; i < samples; i++) {
            for (int x = 0; x < 28; x++) {
                for (int y = 0; y < 28; y++) {
                    inputs[i][x + y * 28] = (images[i].getRGB(x, y) & 0xff) / 255.0;
                }
            }
        }

        int epochs = 1000;
        for (int i = 1; i < epochs; i++) {
            int right = 0;
            double errorSum = 0;
            int batchize = 100;
            for (int j = 0; j < batchize; j++) {
                int imageIndex = (int)(Math.random() * samples);
                double[] targets = new double[10];
                int digit = digits[imageIndex];
                targets[digit] = 1;

                double[] outputs = neuralNetwork.feedForward(inputs[imageIndex]);
                int maxDigit = 0;
                double maxDigitWeight = -1;

                for (int k = 0; k < 10; k++) {
                    if (outputs[k] > maxDigitWeight) {
                        maxDigitWeight = outputs[k];
                        maxDigit = k;
                    }
                }

                if (digit == maxDigit) right++;

                for (int k = 0; k < 10; k++) {
                    errorSum += (targets[k] - outputs[k]) * (targets[k] - outputs[k]);
                }

                neuralNetwork.backpropagation(targets);
            }

            System.out.println("epoch: " + i + ". correct: " + right + ". error: " + errorSum);
        }

        FormDigits f = new FormDigits(neuralNetwork);
        new Thread(f).start();
    }
}
