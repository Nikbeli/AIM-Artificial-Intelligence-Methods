package org.neural;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;

public class FormDigits extends JFrame implements Runnable, MouseListener, MouseMotionListener, KeyListener {
    private final int width = 28;
    private final int height = 28;
    private final int scale = 32;

    private int mousePressed = 0;
    private int mx = 0;
    private int my = 0;
    private double[][] colors = new double[width][height];

    private final BufferedImage image = new BufferedImage(width * scale + 200, height * scale, BufferedImage.TYPE_INT_RGB);
    private final BufferedImage pimage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
    private int frame = 0;

    private final NeuralNetwork neuralNetwork;

    public FormDigits(NeuralNetwork neuralNetwork) {
        this.neuralNetwork = neuralNetwork;
        this.setSize(width * scale + 200 + 16, height * scale + 38);
        this.setVisible(true);
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setLocation(50, 50);
        this.add(new JLabel(new ImageIcon(image)));
        addMouseListener(this);
        addMouseMotionListener(this);
        addKeyListener(this);
    }


    @Override
    public void run() {
        while (true) {
            this.repaint();
            //try { Thread.sleep(17); } catch (InterruptedException e) {}
        }
    }


    @Override
    public void paint(Graphics g) {
        double[] inputs = new double[784];

        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                if (mousePressed != 0) {
                    double dist = (i - mx) * (i - mx) + (j - my) * (j - my);

                    if (dist < 1) dist = 1;
                    dist *= dist;

                    if (mousePressed == 1) colors[i][j] += 0.1 / dist;
                    else colors[i][j] -= 0.1 / dist;

                    if (colors[i][j] > 1) colors[i][j] = 1;
                    if (colors[i][j] < 0) colors[i][j] = 0;
                }

                int color = (int)(colors[i][j] * 255);
                color = (color << 16) | (color << 8) | color;
                pimage.setRGB(i, j, color);
                inputs[i + j * width] = colors[i][j];
            }
        }

        double[] outputs = neuralNetwork.feedForward(inputs);
        int maxDigit = 0;
        double maxDigitWeight = -1;

        for (int i = 0; i < 10; i++) {
            if (outputs[i] > maxDigitWeight) {
                maxDigitWeight = outputs[i];
                maxDigit = i;
            }
        }

        Graphics2D igraph = (Graphics2D) image.getGraphics();
        igraph.drawImage(pimage, 0, 0, width * scale, height * scale, this);
        igraph.setColor(Color.lightGray);
        igraph.fillRect(width * scale + 1, 0, 200, height * scale);
        igraph.setFont(new Font("TimesRoman", Font.BOLD, 48));

        for (int i = 0; i < 10; i++) {
            if (maxDigit == i) igraph.setColor(Color.RED);
            else igraph.setColor(Color.GRAY);

            igraph.drawString(i + ":", width * scale + 20, i * width * scale / 15 + 150);
            Color rectColor = new Color(0, (float)outputs[i], 0);

            int rectWidth = (int)(outputs[i] * 100);
            igraph.setColor(rectColor);
            igraph.fillRect(width * scale + 70, i * width * scale / 15 + 122, rectWidth, 30);
        }

        g.drawImage(image, 8, 30, width * scale + 200, height * scale, this);
        frame++;
    }

    @Override
    public void mouseClicked(MouseEvent e) {

    }

    @Override
    public void mousePressed(MouseEvent e) {
        mousePressed = 1;
        if (e.getButton() == 3) mousePressed = 2;
    }

    @Override
    public void mouseReleased(MouseEvent e) {
        mousePressed = 0;
    }

    @Override
    public void mouseEntered(MouseEvent e) {

    }

    @Override
    public void mouseExited(MouseEvent e) {

    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_SPACE) {
            colors = new double[width][height];
        }
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }

    @Override
    public void mouseDragged(MouseEvent e) {
        mx = e.getX() / scale;
        my = e.getY() / scale;
    }

    @Override
    public void mouseMoved(MouseEvent e) {
        mx = e.getX() / scale;
        my = e.getY() / scale;
    }
}
