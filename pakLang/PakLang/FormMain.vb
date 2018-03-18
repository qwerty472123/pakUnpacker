Imports System.IO
Imports System.Text
Public Class FormMain
    Structure ShowNot
        Dim show As Boolean, t As String
    End Structure
    Dim k As New Dictionary(Of UInt16, ShowNot), cl As BinaryWriter
    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
        If File.Exists(TextBox1.Text) Then
            If Not IsNothing(cl) Then cl.Close()
            k.Clear()
            Dim a As BinaryReader = New BinaryReader(File.OpenRead(TextBox1.Text))
            If a.ReadInt32() <> 4 Then MsgBox("不支持的文件") : Exit Sub
            Dim num = a.ReadInt32()
            If a.ReadByte() <> 1 Then MsgBox("不支持的编码") : Exit Sub
            Dim cl1 As UInt16() = New UInt16(num - 1) {}, cl2 As UInt32() = New UInt32(num - 1) {}
            For i As Long = 0 To num - 1
                cl1(i) = a.ReadUInt16()
                cl2(i) = a.ReadInt32()
            Next i
            Dim dd As ShowNot
            For i As Long = 0 To num - 2
                a.BaseStream.Seek(cl2(i), SeekOrigin.Begin)
                dd.show = False
                dd.t = Encoding.UTF8.GetString(a.ReadBytes(cl2(i + 1) - cl2(i)))
                k.Add(cl1(i), dd)
            Next i
            a.BaseStream.Seek(cl2(num - 1), SeekOrigin.Begin)
            dd.show = True
            dd.t = Encoding.UTF8.GetString(a.ReadBytes(a.BaseStream.Length - cl2(num - 1)))
            k.Add(cl1(num - 1), dd)
            a.Close()
            Dim ff As String = Path.Combine(Path.GetDirectoryName(TextBox1.Text), "en-US.pak")
            If File.Exists(ff) Then
                a = New BinaryReader(File.OpenRead(ff))
                If a.ReadInt32() <> 4 Then lisup() : Exit Sub
                num = a.ReadInt32()
                If a.ReadByte() <> 1 Then lisup() : Exit Sub
                cl1 = New UInt16(num - 1) {}
                cl2 = New UInt32(num - 1) {}
                For i As Long = 0 To num - 1
                    cl1(i) = a.ReadUInt16()
                    cl2(i) = a.ReadInt32()
                Next i
                Dim ts As String
                For i As Long = 0 To num - 2
                    a.BaseStream.Seek(cl2(i), SeekOrigin.Begin)
                    ts = Encoding.UTF8.GetString(a.ReadBytes(cl2(i + 1) - cl2(i)))
                    If k.ContainsKey(cl1(i)) Then
                        If String.Compare(k(cl1(i)).t, ts) = 0 Then
                            dd.show = True
                            dd.t = k(cl1(i)).t
                            k(cl1(i)) = dd
                        End If
                    End If
                Next i
                a.Close()
            End If
            ff = TextBox1.Text & ".cl"
            If (File.Exists(ff)) AndAlso (MsgBox("取读CL文件?", 260) = vbYes) Then
                a = New BinaryReader(File.OpenRead(ff))
                Dim ts As String
                While a.BaseStream.Length > a.BaseStream.Position
                    ts = a.ReadString()
                    dd.show = False
                    dd.t = a.ReadString()
                    k(ts) = dd
                End While
                a.Close()
                cl = New BinaryWriter(File.Open(TextBox1.Text & ".cl", FileMode.Append))
            Else
                UniFile(TextBox1.Text & ".cl")
                cl = New BinaryWriter(File.Open(TextBox1.Text & ".cl", FileMode.Create))
            End If
            lisup()
        Else
            MsgBox("找不到文件")
        End If
        Form1_Resize()
    End Sub
    Private Sub lisup()
        ListView1.Items.Clear()
        For i As Long = 0 To k.Count - 1
            If (CheckBox1.Checked) OrElse (k.Values(i).show) Then ListView1.Items.Add(k.Keys(i)).SubItems.Add(k.Values(i).t)
        Next i
    End Sub
    Private Sub Form1_FormClosed(sender As Object, e As FormClosedEventArgs) Handles Me.FormClosed
        If Not IsNothing(cl) Then cl.Close()
        Diagnostics.Process.GetCurrentProcess().Kill()
    End Sub
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles Me.Load
        Form1_Resize()
    End Sub
    Private Sub Form1_Resize() Handles Me.Resize
        Dim c As Integer = Me.ClientSize.Width - 43 * 3
        TextBox1.Width = c
        TextBox2.Width = c
        TextBox2.Top = Me.ClientSize.Height - 21
        Button4.Location = New Point(Me.ClientSize.Width - 43, Me.ClientSize.Height - 21)
        TextBox2.Size = New Size(Button4.Location)
        TextBox3.Width = c
        TextBox3.Top = Me.ClientSize.Height - 42
        Button5.Location = New Point(Me.ClientSize.Width - 85, Me.ClientSize.Height - 42)
        TextBox3.Size = New Size(Button4.Location)
        CheckBox1.Location = New Point(Me.ClientSize.Width - 42, Me.ClientSize.Height - 40)
        Button1.Left = c
        c += 43
        Button3.Left = c
        c += 43
        Button2.Left = c
        ListView1.Size = New Size(Me.ClientSize.Width, Me.ClientSize.Height - 63)
        ListView1.Columns(1).Width = ListView1.ClientSize.Width - 60
    End Sub
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        OpenFileDialog1.ShowDialog()
    End Sub
    Private Sub OpenFileDialog1_FileOk(sender As Object, e As System.ComponentModel.CancelEventArgs) Handles OpenFileDialog1.FileOk
        TextBox1.Text = OpenFileDialog1.FileName
    End Sub
    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
        If ListView1.SelectedIndices.Count > 0 Then
            For i As Long = 0 To ListView1.SelectedIndices.Count - 1
                Dim kk As ListViewItem = ListView1.Items(ListView1.SelectedIndices.Item(i))
                kk.SubItems.Item(1).Text = TextBox2.Text
                Dim dd As ShowNot
                dd.show = k(kk.SubItems.Item(0).Text).show
                dd.t = TextBox2.Text
                k(kk.SubItems.Item(0).Text) = dd
                cl.Write(kk.SubItems.Item(0).Text)
                cl.Write(dd.t)
            Next i
        End If
    End Sub
    Private Sub ListView1_SelectedIndexChanged(sender As Object, e As EventArgs) Handles ListView1.SelectedIndexChanged
        If ListView1.SelectedIndices.Count > 0 Then TextBox2.Text = ListView1.Items(ListView1.SelectedIndices.Item(0)).SubItems.Item(1).Text
    End Sub
    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
        If ListView1.Items.Count > 0 Then
            Dim v As Integer = 0
            If ListView1.SelectedIndices.Count > 0 Then
                v = ListView1.SelectedIndices.Item(0) + 1
                If v >= ListView1.Items.Count Then Exit Sub
                For i As Long = 0 To ListView1.SelectedIndices.Count - 1
                    ListView1.Items(ListView1.SelectedIndices.Item(i)).Selected = False
                Next i
            End If
            Dim t As ListViewItem = ListView1.FindItemWithText(TextBox3.Text, True, v)
            If Not IsNothing(t) Then
                t.Selected = True
                t.EnsureVisible()
            End If
        End If
    End Sub
    Private Sub CheckBox1_CheckedChanged(sender As Object, e As EventArgs) Handles CheckBox1.CheckedChanged
        lisup()
    End Sub
    Function RemoveExtension(ByVal a As String) As String
        Dim e As Integer = InStrRev(a, ".")
        Return If(e > 0, Mid(a, 1, e - 1), a)
    End Function
    Function UniFile(ByVal a As String) As String
        If File.Exists(a) OrElse Directory.Exists(a) Then
            Dim p As String = RemoveExtension(a) & " 备份", o = Path.GetExtension(a)
            Dim n As String = p & o
            If File.Exists(n) OrElse Directory.Exists(n) Then
                Dim i As Integer = 2
                p = p & "("
                o = ")" & o
                n = p & CStr(i) & o
                While File.Exists(n) OrElse Directory.Exists(n)
                    i += 1
                    n = p & CStr(i) & o
                End While
            End If
            If File.Exists(a) Then
                File.Move(a, n)
            Else
                Directory.Move(a, n)
            End If
        End If
        Return a
    End Function
    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        UniFile(TextBox1.Text)
        Dim a = New BinaryWriter(File.OpenWrite(TextBox1.Text))
        a.Write(CInt(4))
        a.Write(CInt(k.Count))
        a.Write(CByte(1))
        Dim t As Integer = 15 + k.Count * 6, u As Byte()() = New Byte(k.Count - 1)() {}
        For i As Long = 0 To k.Count - 1
            a.Write(k.Keys(i))
            a.Write(t)
            u(i) = Encoding.UTF8.GetBytes(k.Values(i).t)
            t += u(i).Length
        Next i
        a.Write(CShort(0))
        a.Write(CInt(t))
        For i As Long = 0 To k.Count - 1
            a.Write(u(i))
        Next i
        a.Close()
    End Sub
End Class
