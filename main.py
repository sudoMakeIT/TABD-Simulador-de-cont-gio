import argparse
from os import path

#import files
import generate_offsets as go
import generate_contagio as gc
import track_final_bruno as plot_track


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--save", help="Guardar a visualização em vez de mostrar", action="store_true")
    parser.add_argument("-u", "--user", help="Especificar o user da base de dados, default é postgres", default="postgres")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2, 3], help="Modo de apresentação\n1- Mostra só os táxis\n2- Mostra Só os tracks\n3- Mostra táxis e tracks", default="1")
    parser.add_argument("-go", "--generate_offsets", help="Gerar offsets", action="store_true")
    parser.add_argument("-gc", "--generate_contagio", help="Gerar contágio", action="store_true")
    args = parser.parse_args()
    if args.user:
        print("user: " + args.user)
    if args.generate_offsets:
        go.generate_offsets(args.user)
    if args.generate_contagio:
        gc.generate_contagio(args.user)
    if args.mode:
        print("mode: " + str(args.mode))
        #check files
        if(not path.exists("files/offsets3.csv")):
            print("No offset file, python3 main -h")
            exit()
        if(not path.exists("files/lenState.csv") or not path.exists("files/tracks_inf.csv") or not path.exists("files/sizeState.csv") or not path.exists("files/taxis_inf.csv") or not path.exists("files/virusState.csv")):
            print("Contagion files missing, python3 main -h")
            exit()
        plot_track.show_plot(args.user,args.mode)