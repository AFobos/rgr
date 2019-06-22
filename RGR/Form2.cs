using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace RGR
{
    public partial class Form2 : Form
    {
        
        public void set(Form1.cart img)
        {
            pictureBox1.Image = Image.FromFile(@img.View);
            label1.Text = img.Name;
            switch (img.Faction)
            {
                case 0:label2.Text = "Нейтральные";break;
                case 1: label2.Text = "Королевства Севера"; break;
                case 2: label2.Text = "Нильфгаард"; break;
                case 3: label2.Text = "Скоя'тоели"; break;
                case 4: label2.Text = "Чудовища"; break;
                case 5: label2.Text = "Скеллиге"; break;
            }
            switch (img.Heroes)
            {
                case 0: label3.Text = "Обычная"; break;
                case 1: label3.Text = "Герой"; break;
            }
            label4.Text = img.Power.ToString();
            label7.Text = img.Ability;
            label6.Text = img.HTG;
            label13.Text = img.Type;
        }

        public Form2()
        {
            InitializeComponent();
            this.FormBorderStyle = FormBorderStyle.FixedToolWindow;
        }

    }
}
