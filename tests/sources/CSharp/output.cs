
using System;

using System.Collections.Generic;

using System.Text;

using System.Runtime.InteropServices;



namespace ConsoleHelperFunction

{



    public class ConsoleHelper

    {

        [StructLayout(LayoutKind.Sequential)]

        struct POSITION

        {

            public short x;

            public short y;

        }



        
        [DllImport("kernel32.dll", EntryPoint = "GetStdHandle", SetLastError = true, CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]

        private static extern int GetStdHandle(int nStdHandle);



        [DllImport("kernel32.dll", EntryPoint = "SetConsoleCursorPosition", SetLastError = true, CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]

        private static extern int SetConsoleCursorPosition(int hConsoleOutput, POSITION dwCursorPosition);



        public void gotoxy(short x, short y)

        {

            const int STD_OUTPUT_HANDLE = -11;

            int hConsoleHandle = GetStdHandle(STD_OUTPUT_HANDLE);

            POSITION position;

            position.x = x;

            position.y = y;

            SetConsoleCursorPosition(hConsoleHandle, position);

        }



        [StructLayout(LayoutKind.Sequential)]

        struct CONSOLERECT

        {

            public short Left;

            public short Top;

            public short Right;

            public short Bottom;

        }



        [StructLayout(LayoutKind.Sequential)]

        struct CONSOLEBUFFER

        {

            public POSITION size;

            public POSITION position;

            public int attrib;

            public CONSOLERECT window;

            public POSITION maxsize;

        }



        [DllImport("kernel32.dll", EntryPoint = "FillConsoleOutputCharacter", SetLastError = true, CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]

        private static extern int FillConsoleOutputCharacter(int handleConsoleOutput, byte fillchar, int len, POSITION writecord, ref int numberofbyeswritten);



        [DllImport("kernel32.dll", EntryPoint = "GetConsoleScreenBufferInfo", SetLastError = true, CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]

        private static extern int GetConsoleScreenBufferInfo(int handleConsoleOutput, ref CONSOLEBUFFER bufferinfo);


    }

}



namespace CSMarkList

{

    class CStudent

    {

        public string name;

        public int[] marks = new int[5];

        public int total;

    }



    class CStudents

    {

        public string filename = "c:\\csstudents.bin";

        public List<CStudent> m_studList = new List<CStudent>();



        public int m_nMaxStudents;

        public int ReadAllRecords()

        {

            m_studList.Clear();

            m_nMaxStudents = 0;



            if (System.IO.File.Exists(filename) == false)

                return 0;



            System.IO.Stream s1 = System.IO.File.Open(filename, System.IO.FileMode.Open);

            System.IO.BinaryReader f1 = new System.IO.BinaryReader(s1);



            m_nMaxStudents = f1.ReadInt32();



            for (int i = 0; i < m_nMaxStudents; i++)

            {

                CStudent stud = new CStudent();



                stud.name = f1.ReadString();



                for (int j = 0; j < 5; j++)

                    stud.marks[j] = f1.ReadInt32();



                stud.total = f1.ReadInt32();



                m_studList.Add(stud);

            }



            f1.Close();

            return m_nMaxStudents;

        }



        public int WriteAllRecords()

        {

            System.IO.Stream s2 = System.IO.File.Open(filename, System.IO.FileMode.Create);


            for(int i = 0; i < m_nMaxStudents; i++)

            {

                f2.Write(m_studList[i].name);



                for (int j = 0; j < 5; j++)

                    f2.Write(m_studList[i].marks[j]);



                f2.Write(m_studList[i].total);

            }

            f2.Close();

            return m_nMaxStudents;

        }



        public int AddRecord(string name, int[] marks)

        {



            for (int i = 0; i < 5; i++)

                stud.total += stud.marks[i];

            m_studList.Add(stud);

            m_nMaxStudents = m_studList.Count;

            WriteAllRecords();

            return 1;

        }



        public int EditRecord(int index, string name, int[] marks)

        {

            CStudent stud = new CStudent();

            stud.name = name;

            stud.marks = marks;

            stud.total = 0;

            m_studList[index] = stud;

            m_nMaxStudents = m_studList.Count;

            WriteAllRecords();

            return 1;

        }



        public int DeleteRecord(int index)

        {

            m_studList.RemoveAt(index);

            WriteAllRecords();

            return 1;

        }

    }



    class Program

    {



        static void gotoxy(short x, short y)

        {

            ConsoleHelperFunction.ConsoleHelper ch = new ConsoleHelperFunction.ConsoleHelper();

            ch.gotoxy(x, y);

        }



        static void clrscr()

        {

            ConsoleHelperFunction.ConsoleHelper ch = new ConsoleHelperFunction.ConsoleHelper();

            ch.ClearScreen();

        }



        static public int DisplayMainMenu()

        {

            clrscr();



            gotoxy(10,4);

            Console.WriteLine("Welcome to Student MarkList Application");



            gotoxy(10,5);

            Console.WriteLine("___________________________________________");



            gotoxy(10,6);

            Console.WriteLine("1. Add Student Mark List");



            gotoxy(10,7);

            Console.WriteLine("2. Edit Student Mark List");



            gotoxy(10,8);

            Console.WriteLine("3. View Student Mark List");



            gotoxy(10,9);

            Console.WriteLine("4. Delete Student Mark List");



            gotoxy(10,10);

            Console.WriteLine("5. Exit");



            gotoxy(10,11);

            Console.WriteLine("___________________________________________");



            gotoxy(10,13);

            Console.Write("Enter your Selection: ");

            try

            {

                string s = Console.ReadLine();

                return Convert.ToInt32(s);

            }

            catch (Exception e)

            {

                return -1;

            }

        }



        static public void ViewRecords()

        {

            theStudents.ReadAllRecords();



            clrscr();



            gotoxy(10,4);

            Console.WriteLine("Welcome to Student Mark List Application");



            gotoxy(10,5);

            Console.WriteLine("_______________________________________________________________");



            gotoxy(10,6);

            Console.WriteLine("SNo Student Name       Sub1   Sub2   Sub3   Sub4   Sub5   Total");



            gotoxy(10,7);

            Console.WriteLine("_______________________________________________________________");



            int pos = 8;

            
            for(int i = 0; i < theStudents.m_nMaxStudents; i++)

            {

              gotoxy(10,pos);

              Console.WriteLine(i + 1);

              gotoxy(14,pos);

              Console.WriteLine(theStudents.m_studList[i].name);

              gotoxy(33,pos);

              Console.WriteLine(theStudents.m_studList[i].marks[0]);

              gotoxy(40,pos);

              Console.WriteLine(theStudents.m_studList[i].marks[1]);

              gotoxy(47,pos);

              Console.WriteLine(theStudents.m_studList[i].marks[2]);

              gotoxy(54,pos);

              Console.WriteLine(theStudents.m_studList[i].marks[3]);

              gotoxy(61,pos);

              Console.WriteLine(theStudents.m_studList[i].marks[4]);

              gotoxy(68,pos);

              Console.WriteLine(theStudents.m_studList[i].total);

              pos++;

            }

            gotoxy(10,pos++);

            Console.WriteLine("_______________________________________________________________");

            pos++;

            gotoxy(10,pos++);

        }





        static public void InputRecords()

        {

            while(true)

            {

                clrscr();



              gotoxy(10,4);

              Console.WriteLine("Welcome to Student Mark List Application");



                gotoxy(10,5);

              Console.WriteLine("__________________________________________________________");



              gotoxy(10,6);

              Console.WriteLine("Student Name: ");



              gotoxy(10,7);

              Console.WriteLine("Sub1 Mark: ");



              gotoxy(10,8);

              Console.WriteLine("Sub2 Mark: ");



              gotoxy(10,9);

              Console.WriteLine("Sub3 Mark: ");



              gotoxy(10,10);

              Console.WriteLine("Sub4 Mark: ");



              gotoxy(10,11);

              Console.WriteLine("Sub5 Mark: ");



              gotoxy(10,12);

              Console.WriteLine("__________________________________________________________");



              gotoxy(23,6);

              string name;

            name = Console.ReadLine();



            int[] marks = new int[5];

              for(int i = 0; i < 5; i++)

              {

                    gotoxy(23,7 + i);

                marks[i] = Convert.ToInt32(Console.ReadLine());

              }



              theStudents.AddRecord(name, marks);



              gotoxy(10,14);

              Console.WriteLine("Do you want to add another record (Y/N)? ");

            char ch = Console.ReadKey().KeyChar;



              if(ch == 'Y' || ch == 'y')

                  continue;

              else

                  break;

            }

        }





        static public void EditRecords()

        {

            ViewRecords();

            Console.WriteLine("Enter the serial number you want to edit: ");

            int m = Convert.ToInt32(Console.ReadLine()); ;



            if(m >= 1 && m <= theStudents.m_nMaxStudents)

            {

                  clrscr();

                  gotoxy(10,4);

                  Console.WriteLine("Welcome to Student Mark List Application");



                  gotoxy(10,5);

                  Console.WriteLine("__________________________________________________________");



                  gotoxy(10,6);

                  Console.WriteLine("Student Name: ");



                  gotoxy(10,7);

                  Console.WriteLine("Sub1 Mark: ");



                  gotoxy(10,8);

                  Console.WriteLine("Sub2 Mark: ");



                  gotoxy(10,9);

                  Console.WriteLine("Sub3 Mark: ");



                  gotoxy(10,10);

                  Console.WriteLine("Sub4 Mark: ");



                  gotoxy(10,11);

                  Console.WriteLine("Sub5 Mark: ");



                  gotoxy(10,12);

                  Console.WriteLine("__________________________________________________________");



                  gotoxy(23,6);

                  string name;

                name = Console.ReadLine();



                int[] marks = new int[5];

                  for(int i = 0; i < 5; i++)

                  {

                        gotoxy(23,7 + i);

                    marks[i] = Convert.ToInt32(Console.ReadLine());

                  }



                  theStudents.EditRecord(m - 1, name, marks);

                  gotoxy(10,12);

                  Console.WriteLine("Record updated. Press any key to return to Main Menu");

                Console.ReadKey();

            }

            else

            {

                  gotoxy(10,12);

                  Console.WriteLine("Invalid Entry. Press any key to return to Main Menu");

                Console.ReadKey();

            }



        }



        static public void DeleteRecords()

        {

            ViewRecords();

            Console.WriteLine("Enter the serial number you want to delete: ");

            int m = Convert.ToInt32(Console.ReadLine()); ;



            if(m >= 1 && m <= theStudents.m_nMaxStudents)

            {

                theStudents.DeleteRecord(m - 1);

                  Console.WriteLine("Record deleted. Press any key to return to Main Menu");

                Console.ReadKey(); ;

            }

            else

            {

                  Console.WriteLine("Invalid Entry. Press any key to return to Main Menu");

                Console.ReadKey(); ;

            }

        }



        static void Main(string[] args)

        {

            theStudents.ReadAllRecords();

            while(true)

            {

                int selection = DisplayMainMenu();

                if (selection == -1)

                    continue;



            }

        }

    }

}