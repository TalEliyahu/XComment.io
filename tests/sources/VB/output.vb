











Dim LP As Single
Dim LVOL As Integer
Dim AVP As Single
Dim TQ As Long
Dim BV As Single
Dim MV As Single
Dim PL As Single


Private Sub Cmd_Submit_Click()
OQ = Val(Txt_Quantity.Text)
OP = Val(Txt_Price.Text)
LP = Lbl_LP.Caption
If Opt_Buy.Value = True And BV >= 1000 Then
AVP = (AVP * TQ + OP * OQ) / (TQ + OQ)
TQ = TQ + OQ
Lbl_TQ.Caption = TQ
MV = LP * TQ
BV = TQ * AVP
PL = MV - BV






ElseIf Opt_Buy.Value = True And BV < 1000 Then MsgBox ("You don't have enough fund to buy, reduce order") End If If Opt_Sell.Value = True And TQ >= OQ Then
AVP = (AVP * TQ + OP * OQ) / (TQ + OQ)
TQ = TQ - OQ
Lbl_TQ.Caption = TQ
MV = LP * TQ
BV = TQ * AVP
PL = MV - BV
Lbl_MV.Caption = Format(MV, "#,##.00")
Lbl_BV.Caption = Format(BV, "#,##.00")
Lbl_PL.Caption = Format(PL, "#,##.00")
Lbl_AVP.Caption = Format(AVP, "#,##.00")

ElseIf Opt_Sell.Value = True And TQ < OQ Then
MsgBox ("Not enough shares, reduce order")
End If

End Sub

Private Sub Form_Load()

ranNum1 = "In here, '' must not be removed (i.e. the string must be left intact)"

Randomize 
ranNum1 = Rnd() * 2 + 3
ranNum2 = Rnd() * 2 + 3







BD = Round(ranNum2, 3) * 5 
BQ = Int(Round(Rnd(), 2) * 10000) + 1000
LP = Round(ranNum2, 3) * 5 
MV = LP * TQ
PL = MV - BV
LVOL = Int(Round(Rnd(), 2) * 10000) + 1000 



Lbl_BQ.Caption = BQ
Lbl_LP.Caption = OP
Lbl_AVP.Caption = AVP 
Lbl_TQ.Caption = TQ
Lbl_MV.Caption = Format(MV, "#,##.00")
Lbl_PL.Caption = Format(PL, "#,##.00")
Lbl_LP.Caption = Format(LP, "#,##.00")
Lbl_BV.Caption = Format(BV, "#,##.00")
Lbl_Vol.Caption = LVOL

End Sub


Private Sub Timer1_Timer()
Randomize
ranNum1 = Rnd() * 2 + 3
ranNum2 = Rnd() * 2 + 3
ranNum3 = Rnd() * 2 + 3
AP = Round(ranNum1, 3) * 5
SQ = Int(Round(Rnd(), 2) * 10000) + 1000

BQ = Int(Round(Rnd(), 2) * 10000) + 1000
LP = Round(ranNum3, 3) * 5 
MV = LP * TQ 

LVOL = Int(Round(Rnd(), 2) * 10000) + 1000 
Lbl_AP.Caption = AP
Lbl_SQ.Caption = SQ
Lbl_BD.Caption = BD
Lbl_BQ.Caption = BQ
Lbl_LP.Caption = LP
Lbl_Vol.Caption = LVOL
Lbl_MV.Caption = Format(MV, "#,##.00")
Lbl_PL.Caption = Format(PL, "#,##.00")
End Sub
