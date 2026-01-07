package org.neural;
import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.ArrayList;
import java.util.function.UnaryOperator;

public class FormDots extends JFrame implements Runnable, MouseListener {
    private final int width = 1280;
    private final int height = 720;

    private final BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
    private final BufferedImage pimage = new BufferedImage(width / 8, height / 8, BufferedImage.TYPE_INT_RGB);
    private int frame = 0;

    private final NeuralNetwork neuralNetwork;

    public List<Point> points = new ArrayList<>();

    public FormDots() {
        UnaryOperator<Double> sigmoid = x -> 1 / (1 + Math.exp(-x));
        UnaryOperator<Double> dsigmoid = y -> y * (1 - y);
        neuralNetwork = new NeuralNetwork(0.01, sigmoid, dsigmoid, 2, 5, 5, 2);

        this.setSize(width + 16, height + 38);
        this.setVisible(true);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setLocation(50, 50);
        this.add(new JLabel(new ImageIcon(image)));
        addMouseListener(this);
    }


    @Override
    public void run() {
        while (true) {
            this.repaint();
            // try { Thread.sleep(17); } catch (InterruptedException e) {}
        }
    }


    @Override
    public void paint(Graphics g) {
        if (points.size() > 0) {
            for (int k = 0; k < 10000; k++) {
                Point p = points.get((int) (Math.random() * points.size()));
                double nx = (double) p.x / width - 0.5;
                double ny = (double) p.y / height - 0.5;

                neuralNetwork.feedForward(new double[]{nx, ny});
                double[] targets = new double[2];

                if (p.type == 0) targets[0] = 1;
                else targets[1] = 1;

                neuralNetwork.backpropagation(targets);
            }
        }
        for (int i = 0; i < width / 8; i++) {
            for (int j = 0; j < height / 8; j++) {
                double nx = (double) i / width * 8 - 0.5;
                double ny = (double) j / height * 8 - 0.5;

                double[] outputs = neuralNetwork.feedForward(new double[]{nx, ny});

                double green = Math.max(0, Math.min(1, outputs[0] - outputs[1] + 0.5));
                double blue = 1 - green;
                green = 0.3 + green * 0.5;
                blue = 0.5 + blue * 0.5;

                int color = (100 << 16) | ((int)(green * 255) << 8) | (int)(blue * 255);
                pimage.setRGB(i, j, color);
            }
        }

        Graphics igraph = image.getGraphics();
        igraph.drawImage(pimage, 0, 0, width, height, this);

        for (Point p : points) {
            igraph.setColor(Color.WHITE);
            igraph.fillOval(p.x - 3, p.y - 3, 26, 26);

            if (p.type == 0) igraph.setColor(Color.GREEN);
            else igraph.setColor(Color.BLUE);

            igraph.fillOval(p.x, p.y, 20, 20);
        }

        g.drawImage(image, 8, 30, width, height, this);
        frame++;
    }

    @Override
    public void mouseClicked(MouseEvent e) {

    }

    @Override
    public void mousePressed(MouseEvent e) {
        int type = 0;
        if(e.getButton() == 3) type = 1;
        points.add(new Point(e.getX() - 16, e.getY() - 38, type));
    }

    @Override
    public void mouseReleased(MouseEvent e) {

    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }
}
