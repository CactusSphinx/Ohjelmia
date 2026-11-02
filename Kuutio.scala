import scala.math.*
import scala.collection.mutable.Buffer

val tarkkuus = 12
val iteraatiot = 300
val nopeus = 100.0

val L = 10
val w_alpha = 1
val w_beta = 2
val w_gamma = 1

val pisteet = Buffer[Vector[Any]]()

// Päävektorit

val v_x: Double => Double = t => L * (cos(w_alpha * t) * cos(w_beta * t))
val v_y: Double => Double = t => L * (sin(w_alpha * t) * cos(w_beta * t))
val v_z: Double => Double = t => -L * sin(w_beta * t)
val v = Vector(v_x, v_y, v_z)

val w_x: Double => Double = t => L * (cos(w_alpha * t) * sin(w_beta * t) * sin(w_gamma * t) - sin(w_alpha * t) * cos(w_gamma * t))
val w_y: Double => Double = t => L * (sin(w_alpha * t) * sin(w_beta * t) * sin(w_gamma * t) + cos(w_alpha * t) * cos(w_gamma * t))
val w_z: Double => Double = t => L * cos(w_beta * t) * sin(w_gamma * t)
val w = Vector(w_x, w_y, w_z)

val c_x: Double => Double = t => L * (cos(w_alpha * t) * sin(w_beta * t) * cos(w_gamma * t) + sin(w_alpha * t) * sin(w_gamma * t))
val c_y: Double => Double = t => L * (sin(w_alpha * t) * sin(w_beta * t) * cos(w_gamma * t) - cos(w_alpha * t) * sin(w_gamma * t))
val c_z: Double => Double = t => L * cos(w_beta * t) * cos(w_gamma * t)
val c = Vector(c_x, c_y, c_z)

// Vastavektorit

val M_v_x: Double => Double = t => -v_x(t)
val M_v_y: Double => Double = t => -v_y(t)
val M_v_z: Double => Double = t => -v_z(t)
val M_v = Vector(M_v_x, M_v_y, M_v_z)

val M_w_x: Double => Double = t => -w_x(t)
val M_w_y: Double => Double = t => -w_y(t)
val M_w_z: Double => Double = t => -w_z(t)
val M_w = Vector(M_w_x, M_w_y, M_w_z)

val M_c_x: Double => Double = t => -c_x(t)
val M_c_y: Double => Double = t => -c_y(t)
val M_c_z: Double => Double = t => -c_z(t)
val M_c = Vector(M_c_x, M_c_y, M_c_z)


def MuodostaSivu(vektori_1_a: Vector[Double => Double], vektori_2_a: Vector[Double => Double], vektori_3_a: Vector[Double => Double], iteraatio: Double, kirjain: String) =

  val vektori_1 = vektori_1_a.map(komp => komp(iteraatio))
  val vektori_2 = vektori_2_a.map(komp => komp(iteraatio))
  val vektori_3 = vektori_3_a.map(komp => komp(iteraatio))

  val tarkkuus_desim = tarkkuus.toDouble

  for k_1 <- (-tarkkuus).to(tarkkuus) do
    val k = k_1 / tarkkuus_desim
    for l_1 <- (-tarkkuus).to(tarkkuus) do
      val l = l_1 / tarkkuus_desim

      val vektori_x = (vektori_1(0) + k * vektori_2(0) + l * vektori_3(0)).round.toInt
      val vektori_y = (vektori_1(1) + k * vektori_2(1) + l * vektori_3(1)).round.toInt
      val vektori_z = (vektori_1(2) + k * vektori_2(2) + l * vektori_3(2)).round.toInt

      pisteet.append(Vector[Any](vektori_x, vektori_y, vektori_z, kirjain))


@main def Aloitus() =
  for x <- 1 to iteraatiot do
    pisteet.clear()

    MuodostaSivu(v, w, c, x / nopeus, "*")
    MuodostaSivu(w, v, c, x / nopeus, "-")
    MuodostaSivu(c, w, v, x / nopeus, "$")

    MuodostaSivu(M_v, M_w, M_c, x / nopeus, "/")
    MuodostaSivu(M_w, M_v, M_c, x / nopeus, ".")
    MuodostaSivu(M_c, M_w, M_v, x / nopeus, "€")

    val skaalaus = 4

    var tulostuslista = Array.ofDim[String](skaalaus * L, skaalaus * L)

      for rivi <- 0.to(skaalaus * L - 1) do
        val ehto2 = (rivi - skaalaus / 2.0 * L).round

        for sarake <- 0.to(skaalaus * L - 1) do
          val ehto1 = (sarake - skaalaus / 2.0 * L).round
          var ehdokkaat = Buffer[Vector[Any]]()

            for piste <- pisteet do
              if piste(0) == ehto1 && piste(1) == ehto2 then
                ehdokkaat.append(Vector[Any](piste(2), piste(3)))

          if !ehdokkaat.isEmpty then
            var suurin = ehdokkaat(0)(0)
            var lisättävä = ehdokkaat(0)(1)

            for ehdokas <- ehdokkaat do
              if ehdokas(0).asInstanceOf[Int] > suurin.asInstanceOf[Int] then
                suurin = ehdokas(0)
                lisättävä = ehdokas(1)

              tulostuslista(rivi)(sarake) = lisättävä.asInstanceOf[String]

            else
              tulostuslista(rivi)(sarake) = " "

    print("\u001b[2J\u001b[H")
    System.out.flush()

    tulostuslista.foreach(rivi => println(rivi.toVector.mkString("")))
