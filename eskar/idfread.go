package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	Floor   = iota
	Wall    = iota
	Ceiling = iota
	Roof    = iota
)

const (
	Adiabatic                              = iota
	Surface                                = iota
	Zone                                   = iota
	Outdoors                               = iota
	Foundation                             = iota
	Ground                                 = iota
	GroundFCfactorMethod                   = iota
	OtherSideCoefficient                   = iota
	OtherSideConditionsModel               = iota
	GroundSlabPreprocessorAverage          = iota
	GroundSlabPreprocessorCore             = iota
	GroundSlabPreprocessorPerimeter        = iota
	GroundBasementPreprocessorAverageWall  = iota
	GroundBasementPreprocessorAverageFloor = iota
	GroundBasementPreprocessorUpperWall    = iota
	GroundBasementPreprocessorLowerWall    = iota
)

type Vertex struct {
	XCoord float64
	YCoord float64
	ZCoord float64
}

type BuildSurfDetType struct {
	Name         string
	SurfType     int
	ConsNm       string
	ZoneNm       string
	OutBndCond   string
	OutBndCondNm string
	SunExposed   bool
	WindExposed  bool
	ViewFact     float64
	NumVert      int
	Vertices     []Vertex
}

var buildSurfDet []BuildSurfDetType

func main() {
	var foundObjects []string
	foundObjects = readidf5("5ZoneAirCooled.idf", "modified.idf")
	showFound(foundObjects)
}

func readidf5(infilename string, outfilename string) ([]string){

	var foundObjects []string

	infile, err := os.Open(infilename)
	if err != nil {
		log.Fatal(err)
	}
	defer infile.Close()
	scanner := bufio.NewScanner(infile)

	outfile, err := os.Create(outfilename)
	if err != nil {
		log.Fatal("cannot create file", err)
	}
	defer outfile.Close()

	withinObject := false
	withinSelectedObject := false
	var objStringBuilder strings.Builder

	for scanner.Scan() {
		linein := scanner.Text()
		exclaimPos := strings.Index(linein, "!")

		var lineNoComment string
		if exclaimPos != -1 {
			lineNoComment = linein[:exclaimPos]
		} else {
			lineNoComment = linein
		}

		commaLoc := strings.Index(lineNoComment, ",")
		semiLoc := strings.Index(lineNoComment, ";")

		objStringBuilder.WriteString(strings.TrimSpace(lineNoComment))

		if !withinObject && commaLoc != -1 {
			withinObject = true
			lineParts := strings.Split(lineNoComment, ",")
			if strings.TrimSpace(lineParts[0]) == "BuildingSurface:Detailed" {
				withinSelectedObject = true
			}
		}

		if withinSelectedObject {
			fmt.Fprintln(outfile, "!    ", linein)
		} else {
			fmt.Fprintln(outfile, linein)
		}

		if semiLoc != -1 {
			withinObject = false
			withinSelectedObject = false
			objString := objStringBuilder.String()
			objString = strings.TrimRight(objString, ";")
			objParts := strings.Split(objString, ",")
			if objParts[0] == "BuildingSurface:Detailed" {
				foundObjects = append(foundObjects, objString)
				// fmt.Fprintln(outfile, objParts[0])
				// fmt.Fprintln(outfile, objParts[1])
			}
			objStringBuilder.Reset()
		}
	}
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
  return foundObjects
}

func showFound(foundObjects []string){
	for _, obj := range foundObjects {
		fields := strings.Split(obj, ",")
		var bsd BuildSurfDetType
		bsd.Name = fields[1]
		// bsd.SurfType
		bsd.ConsNm = fields[3]
		bsd.ZoneNm = fields[4]
		// bsd.OutBndCond
		bsd.OutBndCondNm = fields[6]
		//bsd.SunExposed
		//bsd.WindExposed
		viewFactor, err := strconv.ParseFloat(fields[9], 64)
		bsd.ViewFact = viewFactor
		bsd.NumVert, err = strconv.Atoi(fields[10])
		//bsd.Vertices[0].XCoord =
		buildSurfDet = append(buildSurfDet, bsd)
		log.Fatal(err)
	}

	for _, obj := range buildSurfDet {
		fmt.Println(obj.Name, "::", obj.ZoneNm, "::", obj.ConsNm)
	}
	
}
